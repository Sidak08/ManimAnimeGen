import os
import ast
import json
import sys
import re
from collections import defaultdict

class ManimSceneAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.scenes = {}
        self.current_scene = None
        self.current_method = None
        self.animations = []
        self.objects = {}
        self.steps = []
        
    def visit_ClassDef(self, node):
        # Only process Scene subclasses
        is_scene = False
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id == 'Scene':
                is_scene = True
            elif isinstance(base, ast.Name) and 'Scene' in base.id:  # For other scene types like ThreeDScene
                is_scene = True
                
        if is_scene:
            self.current_scene = node.name
            self.scenes[node.name] = {
                'objects': {},
                'animations': [],
                'steps': []
            }
            
        # Continue visiting child nodes
        self.generic_visit(node)
        self.current_scene = None
    
    def visit_FunctionDef(self, node):
        if self.current_scene and node.name == 'construct':
            self.current_method = 'construct'
            self.generic_visit(node)
            self.current_method = None
        else:
            self.generic_visit(node)
    
    def visit_Assign(self, node):
        if not self.current_scene or not self.current_method:
            self.generic_visit(node)
            return
            
        # Extract variable assignments to track created objects
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id
                
                # Try to determine the object type and properties
                obj_info = self._extract_object_info(node.value)
                if obj_info:
                    self.scenes[self.current_scene]['objects'][var_name] = obj_info
        
        self.generic_visit(node)
    
    def visit_Expr(self, node):
        if not self.current_scene or not self.current_method:
            return
            
        # Look for self.play(...) calls
        if isinstance(node.value, ast.Call):
            func = node.value.func
            if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
                if func.value.id == 'self' and func.attr == 'play':
                    animation_info = self._extract_animation_info(node.value)
                    if animation_info:
                        self.scenes[self.current_scene]['animations'].append(animation_info)
                        self.scenes[self.current_scene]['steps'].append({
                            'type': 'animation',
                            'data': animation_info
                        })
                elif func.value.id == 'self' and func.attr == 'wait':
                    # Track wait commands as well
                    self.scenes[self.current_scene]['steps'].append({
                        'type': 'wait',
                        'duration': self._get_arg_value(node.value.args[0]) if node.value.args else 1
                    })
        
        self.generic_visit(node)
        
    def _extract_object_info(self, node):
        """Extract type and properties of created objects"""
        if isinstance(node, ast.Call):
            obj_type = None
            if isinstance(node.func, ast.Name):
                obj_type = node.func.id
            elif isinstance(node.func, ast.Attribute):
                obj_type = node.func.attr
                
            if obj_type:
                # Extract args and kwargs
                args = []
                kwargs = {}
                
                # Process positional args
                for arg in node.args:
                    arg_val = self._get_arg_value(arg)
                    if arg_val is not None:
                        args.append(arg_val)
                
                # Process keyword args
                for keyword in node.keywords:
                    kwarg_val = self._get_arg_value(keyword.value)
                    if kwarg_val is not None:
                        kwargs[keyword.arg] = kwarg_val
                
                return {
                    'type': obj_type,
                    'args': args,
                    'kwargs': kwargs
                }
        return None
    
    def _extract_animation_info(self, node):
        """Extract information about animation calls"""
        animations = []
        
        for arg in node.args:
            if isinstance(arg, ast.Call):
                anim_type = None
                if isinstance(arg.func, ast.Name):
                    anim_type = arg.func.id
                elif isinstance(arg.func, ast.Attribute):
                    anim_type = arg.func.attr
                
                if anim_type:
                    # Extract animation targets and parameters
                    anim_args = []
                    anim_kwargs = {}
                    
                    for sub_arg in arg.args:
                        arg_val = self._get_arg_value(sub_arg)
                        if arg_val is not None:
                            anim_args.append(arg_val)
                    
                    for keyword in arg.keywords:
                        kwarg_val = self._get_arg_value(keyword.value)
                        if kwarg_val is not None:
                            anim_kwargs[keyword.arg] = kwarg_val
                    
                    animations.append({
                        'type': anim_type,
                        'args': anim_args,
                        'kwargs': anim_kwargs
                    })
            elif isinstance(arg, ast.Attribute) and isinstance(arg.value, ast.Name):
                # This might be an object reference like my_object.animate.method()
                animations.append({
                    'type': 'object_animation',
                    'object': arg.value.id,
                    'method': arg.attr
                })
        
        # Look for keyword arguments in the play method itself (like run_time)
        play_kwargs = {}
        for keyword in node.keywords:
            kwarg_val = self._get_arg_value(keyword.value)
            if kwarg_val is not None:
                play_kwargs[keyword.arg] = kwarg_val
        
        return {
            'animations': animations,
            'kwargs': play_kwargs
        }
    
    def _get_arg_value(self, node):
        """Extract literal values from AST nodes"""
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.NameConstant):
            return node.value
        elif isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.Name):
            return node.id  # This returns the variable name as a string
        elif isinstance(node, ast.List):
            return [self._get_arg_value(elt) for elt in node.elts]
        elif isinstance(node, ast.Tuple):
            return tuple(self._get_arg_value(elt) for elt in node.elts)
        elif isinstance(node, ast.Dict):
            return {
                self._get_arg_value(key): self._get_arg_value(value) 
                for key, value in zip(node.keys, node.values)
            }
        elif isinstance(node, ast.Call):
            # For nested calls, just provide the function name with a note that it's a call
            if isinstance(node.func, ast.Name):
                return f"call:{node.func.id}"
            elif isinstance(node.func, ast.Attribute):
                return f"call:{node.func.attr}"
        return None

def process_manim_file(file_path):
    """Process a Manim Python file to extract scene information"""
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    try:
        tree = ast.parse(code)
        analyzer = ManimSceneAnalyzer()
        analyzer.visit(tree)
        return analyzer.scenes
    except SyntaxError as e:
        print(f"Syntax error in file {file_path}: {e}")
        return {}

def extract_source_code_blocks(scenes_data, file_path):
    """Extract the actual source code blocks corresponding to each scene and animation step"""
    with open(file_path, 'r', encoding='utf-8') as f:
        source_lines = f.readlines()
    
    # Use regex to find class definitions and methods
    class_pattern = re.compile(r'class\s+(\w+)\s*\([^)]*\):')
    
    line_idx = 0
    scene_source = {}
    
    while line_idx < len(source_lines):
        line = source_lines[line_idx]
        class_match = class_pattern.match(line)
        if class_match:
            class_name = class_match.group(1)
            if class_name in scenes_data:
                # Found a scene class, collect its source code
                start_line = line_idx
                # Find the end of this class definition
                depth = 0
                end_line = start_line
                
                # Simple heuristic to find class end - assumes proper indentation
                while end_line < len(source_lines):
                    if re.match(r'class\s+', source_lines[end_line]):
                        if end_line > start_line:  # Skip the initial class line
                            break
                    end_line += 1
                
                scene_source[class_name] = ''.join(source_lines[start_line:end_line])
        line_idx += 1
    
    return scene_source

def main():
    """Process all Manim files in the specified directory"""
    if len(sys.argv) < 2:
        print("Usage: python auto_labeler.py <directory_or_file>")
        return
    
    target_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "manim_dataset.json"
    
    dataset = []
    
    if os.path.isdir(target_path):
        # Process all Python files in the directory
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    print(f"Processing {file_path}")
                    try:
                        scenes_data = process_manim_file(file_path)
                        source_blocks = extract_source_code_blocks(scenes_data, file_path)
                        
                        for scene_name, scene_info in scenes_data.items():
                            if scene_name in source_blocks:
                                dataset.append({
                                    'file': file_path,
                                    'scene_name': scene_name,
                                    'source_code': source_blocks[scene_name],
                                    'objects': scene_info['objects'],
                                    'animations': scene_info['animations'],
                                    'steps': scene_info['steps']
                                })
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
    elif os.path.isfile(target_path) and target_path.endswith('.py'):
        # Process a single file
        try:
            file_path = target_path
            scenes_data = process_manim_file(file_path)
            source_blocks = extract_source_code_blocks(scenes_data, file_path)
            
            for scene_name, scene_info in scenes_data.items():
                if scene_name in source_blocks:
                    dataset.append({
                        'file': file_path,
                        'scene_name': scene_name,
                        'source_code': source_blocks[scene_name],
                        'objects': scene_info['objects'],
                        'animations': scene_info['animations'],
                        'steps': scene_info['steps']
                    })
        except Exception as e:
            print(f"Error processing {target_path}: {e}")
    else:
        print(f"Invalid path: {target_path}")
        return
    
    # Save the dataset to a JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2)
    
    print(f"Dataset saved to {output_path} with {len(dataset)} scenes")

if __name__ == "__main__":
    main()