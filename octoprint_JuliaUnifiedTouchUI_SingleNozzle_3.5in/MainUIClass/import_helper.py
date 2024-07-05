import importlib.util
import os

def load_and_assign_functions(directory, cls):
    def assign_to_class(func):
        setattr(cls, func.__name__, func)
    
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            module_name = filename[:-3]
            file_path = os.path.join(directory, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for name, value in module.__dict__.items():
                if callable(value) and not name.startswith("__"):
                    assign_to_class(value)

def load_classes(directory):
    classes = {}
    
    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            file_path = os.path.join(directory, filename)
            
            #print(f"Processing file: {file_path}")
            
            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                #print(f"Successfully loaded module: {module_name}")
                
                for name, obj in module.__dict__.items():
                    if isinstance(obj, type):
                        classes[name] = obj
                        #print(f"Found class: {name} in module: {module_name}")
            except Exception as e:
                pass
                #print(f"Failed to load module {module_name}: {e}")
    
    return classes