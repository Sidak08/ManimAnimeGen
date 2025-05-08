import os
import json
import re
import sys
from collections import defaultdict

def extract_math_expressions(source_code):
    """Extract mathematical expressions from MathTex and Tex objects"""
    # Look for patterns like MathTex(r"...") or Tex(r"...")
    mathtex_pattern = re.compile(r'(?:MathTex|Tex)\s*\(\s*r?[\'"]([^\'"]+)[\'"]')
    matches = mathtex_pattern.findall(source_code)
    
    expressions = []
    for match in matches:
        # Clean up the expression
        expr = match.strip()
        # Add the expression if it's not empty
        if expr:
            expressions.append(expr)
    
    return expressions

def categorize_math_content(expressions):
    """Categorize mathematical content by subject area"""
    categories = defaultdict(list)
    
    # Define patterns for different mathematical subjects
    patterns = {
        'calculus': [r'\\int', r'\\sum', r'\\lim', r'd[fx]', r'\\nabla', r'\\partial'],
        'linear_algebra': [r'\\begin\{bmatrix\}', r'\\vec', r'\\matrix', r'\\det', r'\\Rightarrow'],
        'geometry': [r'\\triangle', r'\\angle', r'\\circle', r'\\perp', r'\\parallel'],
        'complex_analysis': [r'\\mathds\{C\}', r'\\arg', r'z', r'\\overline\{z\}', r'e\\^\{i\}'],
        'trigonometry': [r'\\sin', r'\\cos', r'\\tan', r'\\theta', r'\\pi'],
        'probability': [r'P\\', r'\\mathbb\{E\}', r'\\mathbb\{P\}', r'\\sigma', r'\\mu'],
        'combinatorics': [r'\\binom', r'\\choose', r'n!', r'\\mathcal\{P\}'],
    }
    
    for expr in expressions:
        categorized = False
        for category, patterns_list in patterns.items():
            for pattern in patterns_list:
                if re.search(pattern, expr):
                    categories[category].append(expr)
                    categorized = True
                    break
            if categorized:
                break
        if not categorized:
            categories['other'].append(expr)
    
    return dict(categories)

def identify_key_concepts(source_code, expressions):
    """Identify key mathematical concepts in the code"""
    concepts = []
    
    # Look for comments explaining concepts
    comment_pattern = re.compile(r'#\s*(.+)$', re.MULTILINE)
    comments = comment_pattern.findall(source_code)
    
    # Filter comments that might explain concepts
    concept_keywords = ['concept', 'theorem', 'lemma', 'property', 'rule', 'law', 'identity', 'formula']
    for comment in comments:
        for keyword in concept_keywords:
            if keyword in comment.lower():
                concepts.append(comment.strip())
                break
    
    return concepts

def enhance_dataset_with_math_labels(dataset_path, output_path):
    """Add math-specific labels to the dataset"""
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    enhanced_dataset = []
    
    for scene_data in dataset:
        source_code = scene_data['source_code']
        
        # Extract math expressions
        expressions = extract_math_expressions(source_code)
        
        # Categorize math content
        math_categories = categorize_math_content(expressions)
        
        # Identify key concepts
        concepts = identify_key_concepts(source_code, expressions)
        
        # Add math-specific labels
        enhanced_scene = scene_data.copy()
        enhanced_scene['math_labels'] = {
            'expressions': expressions,
            'categories': math_categories,
            'concepts': concepts,
        }
        
        # Determine primary math domain
        if math_categories:
            primary_domain = max(math_categories, key=lambda k: len(math_categories[k]) if k != 'other' else -1)
            if primary_domain == 'other' and math_categories.get('other', []):
                # Try to find the second most common domain
                domains = [(k, len(v)) for k, v in math_categories.items() if k != 'other']
                if domains:
                    domains.sort(key=lambda x: x[1], reverse=True)
                    primary_domain = domains[0][0]
            
            enhanced_scene['math_labels']['primary_domain'] = primary_domain
        
        enhanced_dataset.append(enhanced_scene)
    
    # Save the enhanced dataset
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enhanced_dataset, f, indent=2)
    
    print(f"Enhanced dataset saved to {output_path} with {len(enhanced_dataset)} scenes")

def main():
    """Process the dataset to add math-specific labels"""
    if len(sys.argv) < 2:
        print("Usage: python math_labeler.py <dataset_path> [output_path]")
        return
    
    dataset_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "manim_math_dataset.json"
    
    enhance_dataset_with_math_labels(dataset_path, output_path)

if __name__ == "__main__":
    main()