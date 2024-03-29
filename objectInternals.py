"""
Useful core Python attribute functions

getattr(class, attribute)
setattr(class, attribute)
delattr(class, attribute)

"""


class Vector:
    """
    A n-dimensional vector
    """

    def __init__(self, **components):
        '''
        **components argument offers customization of input arguments
        by hashing them to the __dict__ class attribute. These are known as
        dynamic class attributes.

        The dictionary comprehension appends an underscore in front of the dictionary key
        to be within the nomenclature of being an immutable class attribute.
        '''
        private_components = {
            f"_{k}" : v for k,v in components.items()

        }
        self.__dict__.update(private_components)

    def __getattr__(self, name):
        '''
        Invoked after a failed attribute lookup. 
        This is required to grant read access to
        the immutable attribute.
        '''
        private_name = f"_{name=}"
        try:
            self.__dict__[private_name] # Checks to see if attribute is in the class dictionary
        except KeyError:
            raise AttributeError(f"{self!r} object has not attribute {name!r}") # Raises error if attribute does not exist
        # This removes the potential for Maximum Recursion Depth error raise from non-existent attribute calls
        return getattr(self, private_name)
        
    def __setattr__(self, name, value):
        '''
        Raises an attribute error whenever a user attempts to
        overwrite the immutable attribute. Effectively preventing read
        access to the custom attribute.
        '''
        raise AttributeError(f'Cannot set attribute {name!r}')

    def __repr__(self):
        """
        __repr__ is a special method used to represent a class's 
        objects as a string. __repr__ is called by the repr() built-in function. 
        You can define your own string representation of your class objects using the __repr__ method
        """
        return '{} ({})'.format(
            type(self).__name__, # The first part of the format argument
            ', '.join(           # join loop of the key value pairs in the __dict__ class attribute
                "{k} = {v}".format(
                    k=k[1:], # Excludes the underscore of the immutable attribute
                    v=v,
                ) for k,v in self.__dict__.items()
            )
        )
