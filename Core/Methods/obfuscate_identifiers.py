import ast
import random
import string
import astor
from Core.Utils.exclusions import EXCLUDED_NAMES
from Core.utils import name_generator  # Import the name_generator instance

class ObfuscateIdentifiers(ast.NodeTransformer):
    def __init__(self):
        self.name_mapping = {}
        self.specific_names = {'is_present', 'loader', 'encodeddata', 'secretkey', 'encryptedcode', 'dummyoperation', 'actualhash', 'c', 'd', 'i', 'e', 's', 'decryptedcode', 'secureexec', 'encrypteddata', 'expectedhash', 'decompresseddata', 'marshalleddata', 'ciphersuite', 'decrypteddata', 'finaldata', 'key', 'result', 'dummylist', 'execfunc', 'data'}  # Add specific names to target
        self.semi_specific_names = {'junk', 'part'}  # Add base names to target

    def generate_name(self, original_name):
        if original_name not in self.name_mapping:
            self.name_mapping[original_name] = name_generator.generate_name()
        return self.name_mapping[original_name]

    def is_semi_specific(self, name):
        for base in self.semi_specific_names:
            if base in name:
                return True
        return False

    def should_exclude(self, name):
        return name in EXCLUDED_NAMES or (name.startswith('__') and name.endswith('__'))

    def visit_ClassDef(self, node):
        original_name = node.name
        if not self.should_exclude(original_name) and not self.is_semi_specific(original_name):
            new_name = self.generate_name(original_name)
            self.name_mapping[original_name] = new_name
            node.name = new_name
        elif self.is_semi_specific(original_name):
            new_name = self.generate_name(original_name)
            self.name_mapping[original_name] = new_name
            node.name = new_name
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        original_name = node.name
        if not self.should_exclude(original_name) and not self.is_semi_specific(original_name):
            new_name = self.generate_name(original_name)
            self.name_mapping[original_name] = new_name
            node.name = new_name
        elif self.is_semi_specific(original_name):
            new_name = self.generate_name(original_name)
            self.name_mapping[original_name] = new_name
            node.name = new_name

        # Rename function parameters if they are in specific_names or semi-specific
        node.args.args = [self.visit(arg) for arg in node.args.args]
        self.generic_visit(node)
        return node

    def visit_arg(self, node):
        if node.arg in self.specific_names:
            node.arg = self.generate_name(node.arg)
        elif self.is_semi_specific(node.arg):
            node.arg = self.generate_name(node.arg)
        return node

    def visit_Name(self, node):
        if node.id in self.name_mapping:
            node.id = self.name_mapping[node.id]
        elif node.id in self.specific_names:
            node.id = self.generate_name(node.id)
        elif self.is_semi_specific(node.id):
            node.id = self.generate_name(node.id)
        return node

    def visit_Attribute(self, node):
        if node.attr in self.name_mapping:
            node.attr = self.name_mapping[node.attr]
        elif node.attr in self.specific_names:
            node.attr = self.generate_name(node.attr)
        elif self.is_semi_specific(node.attr):
            node.attr = self.generate_name(node.attr)
        self.generic_visit(node)
        return node

    def visit_Assign(self, node):
        self.generic_visit(node)
        for target in node.targets:
            if isinstance(target, ast.Name):
                if target.id in self.name_mapping:
                    target.id = self.name_mapping[target.id]
                elif target.id in self.specific_names:
                    target.id = self.generate_name(target.id)
                elif self.is_semi_specific(target.id):
                    target.id = self.generate_name(target.id)
            elif isinstance(target, ast.Attribute):
                if target.attr in self.name_mapping:
                    target.attr = self.name_mapping[target.attr]
                elif target.attr in self.specific_names:
                    target.attr = self.generate_name(target.attr)
                elif self.is_semi_specific(target.attr):
                    target.attr = self.generate_name(target.attr)
        if isinstance(node.value, ast.Name):
            if node.value.id in self.name_mapping:
                node.value.id = self.name_mapping[node.value.id]
            elif node.value.id in self.specific_names:
                node.value.id = self.generate_name(node.value.id)
            elif self.is_semi_specific(node.value.id):
                node.value.id = self.generate_name(node.value.id)
        elif isinstance(node.value, ast.Attribute):
            if node.value.attr in self.name_mapping:
                node.value.attr = self.name_mapping[node.value.attr]
            elif node.value.attr in self.specific_names:
                node.value.attr = self.generate_name(node.value.attr)
            elif self.is_semi_specific(node.value.attr):
                node.value.attr = self.generate_name(node.value.attr)
        return node

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in self.name_mapping:
                node.func.id = self.name_mapping[node.func.id]
            elif node.func.id in self.specific_names:
                node.func.id = self.generate_name(node.func.id)
            elif self.is_semi_specific(node.func.id):
                node.func.id = self.generate_name(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            if node.func.attr in self.name_mapping:
                node.func.attr = self.name_mapping[node.func.attr]
            elif node.func.attr in self.specific_names:
                node.func.attr = self.generate_name(node.func.attr)
            elif self.is_semi_specific(node.func.attr):
                node.func.attr = self.generate_name(node.func.attr)
        self.generic_visit(node)
        return node

def obfuscate_identifiers(code):
    tree = ast.parse(code)
    obfuscator = ObfuscateIdentifiers()
    obfuscator.visit(tree)

    # Ensure that all function references are renamed
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for sub_node in ast.walk(node):
                if isinstance(sub_node, ast.Name) and sub_node.id in obfuscator.name_mapping:
                    sub_node.id = obfuscator.name_mapping[sub_node.id]
                if isinstance(sub_node, ast.Attribute) and sub_node.attr in obfuscator.name_mapping:
                    sub_node.attr = obfuscator.name_mapping[sub_node.attr]

    return astor.to_source(tree)
