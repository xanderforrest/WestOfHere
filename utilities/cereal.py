class Cereal:
    @staticmethod
    def serialise(obj, ref):
        """ Serialise an object against the default reference of that object,
        to reduce the amount of data that needs to be stored """

        obj_attrs = vars(obj)
        ref_attrs = vars(ref)

        unique_attrs = {}

        for key in ref_attrs:
            if ref_attrs[key] != obj_attrs[key]:
                unique_attrs[key] = obj_attrs[key]

        return unique_attrs

    @staticmethod
    def deserialise(data, ref):  #  christ, what a method name
        """ Returns an instantiated object with the attributes from the deseralised data """

        for key in data:
            ref.key = data[key]

        return ref
