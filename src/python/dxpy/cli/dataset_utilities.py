from ..bindings import DXRecord
from ..utils.resolver import resolve_existing_path
from ..bindings.dxdataobject_functions import is_dxlink
from ..bindings.dxfile import DXFile
from ..utils.file_handle import as_handle
import sys
import collections
import json
import pandas as pd
import os

def extract_dataset(args):
    project, path, entity_result = resolve_existing_path(args.path)
    rec = DXDataset(entity_result['id'],project=project)
    rec_json = rec.get_descriptor()
    rec_dict = rec.get_dictionary().write(output_path="")
    
class DXDataset(DXRecord):
    """
    Generalized object model for DNAnexus datasets.
    Attributes:
    """

    _record_type = "Dataset"

    def __init__(self, dxid=None, project=None):
        DXRecord.__init__(self,dxid=dxid)
        self.describe(default_fields=True, fields={'properties', 'details'})
        assert DXDataset._record_type in self.types
        assert 'descriptor' in self.details
        if is_dxlink(self.details['descriptor']):
           self.descriptor_dxfile = DXFile(self.details['descriptor'], mode='rb')
        # else:
        #     raise DXError(TODO: )
        self.descriptor = None
        self.name = self.details.get('name')
        self.description = self.details.get('description')
        self.schema = self.details.get('schema')
        self.version = self.details.get('version')
    
    def get_descriptor(self):
        if self.descriptor is None:
            self.descriptor = DXDatasetDescriptor(self.descriptor_dxfile,schema=self.schema)

        return self.descriptor

    def get_dictionary(self):
        if self.descriptor is None:
            self.get_descriptor()

        return self.descriptor.get_dictionary()

class DXDatasetDescriptor():

    def __init__(self, dxfile, **kwargs):
        python3_5_x = sys.version_info.major == 3 and sys.version_info.minor == 5

        with as_handle(dxfile, is_gzip=True, **kwargs) as f:
            if python3_5_x:
                jsonstr = f.read()
                if type(jsonstr) != str:
                    jsonstr = jsonstr.decode("utf-8")

                obj = json.loads(jsonstr, object_pairs_hook=collections.OrderedDict)
            else:
                obj = json.load(f, object_pairs_hook=collections.OrderedDict)
        
        for key in obj:
            setattr(self,key, obj[key])
        self.schema = kwargs.get('schema')

    def get_dictionary(self):
        return DXDatasetDictionary(self)

class DXDatasetDictionary():
    def __init__(self, descriptor):
        self.data_dictionary =  self.load_data_dictionary(descriptor)
        self.coding_dictionary = self.load_coding_dictionary(descriptor)
        self.entity_dictionary = self.load_entity_dictionary(descriptor)
    
    def load_data_dictionary(self, descriptor):
        eblocks = collections.OrderedDict()
        for entity_name in descriptor.model['entities']:
            eblocks[entity_name] = self.create_entity_dframe(descriptor.model['entities'][entity_name])
        print(eblocks)

    def create_entity_dframe(self, entity):
        required_columns = [
            "entity", 
            "name", 
            "type" 
            #"primary_key_type"
        ]

        extra_cols = [
            "coding_name",
            "concept",
            "description",
            "folder_path",
            "is_multi_select",
            "is_sparse_coding",
            "linkout",
            #"longitudinal_axis_type",
            #"referenced_entity_field",
            #"relationship",
            "title",
            "units",
        ]
        dcols = {col: [] for col in required_columns + extra_cols}
        dcols["entity"] = [entity["name"]] * len(entity["fields"])
        dcols["referenced_entity_field"] = [""] * len(entity["fields"])

        for field in entity["fields"]:
            # Field-level parameters
            dcols["name"].append(entity["fields"][field]["name"])
            dcols["type"].append(entity["fields"][field]["type"])
            
            # Optional cols to be filled in with blanks regardless
            dcols["coding_name"].append(entity["fields"][field]["coding_name"] if entity["fields"][field]["coding_name"] else "")
            dcols["concept"].append(entity["fields"][field]["concept"])
            dcols["description"].append(entity["fields"][field]["description"])
            dcols["folder_path"].append(
                " > ".join(entity["fields"][field]["folder_path"])
                if ("folder_path" in entity["fields"][field].keys() and entity["fields"][field]["folder_path"])
                else "")
            dcols["is_multi_select"].append("yes" if entity["fields"][field]["is_multi_select"] else "")
            dcols["is_sparse_coding"].append("yes" if entity["fields"][field]["is_sparse_coding"] else "")
            dcols["linkout"].append(entity["fields"][field]["linkout"])
            dcols["title"].append(entity["fields"][field]["title"])
            dcols["units"].append(entity["fields"][field]["units"])

        try:
            dframe = pd.DataFrame(dcols)
        except ValueError as exc:
            print({key: len(vals) for key, vals in dcols.items()},
                  file=sys.stderr)
            raise exc
        
        return dframe

    def load_coding_dictionary(self, descriptor):
        cblocks = collections.OrderedDict()
        for entity in descriptor.model['entities']:
            for field in descriptor.model['entities'][entity]["fields"]:
                if descriptor.model['entities'][entity]["fields"][field]["coding_name"] and \
                   descriptor.model['entities'][entity]["fields"][field]["coding_name"] not in cblocks:
                    cblocks[descriptor.model['entities'][entity]["fields"][field]["coding_name"]] = \
                        self.create_coding_name_dframe(descriptor.model, entity, field, \
                                                       descriptor.model['entities'][entity]["fields"][field]["coding_name"])
        return cblocks

    def create_coding_name_dframe(self, model, entity, field, code):
        dcols = {}
        if model['entities'][entity]["fields"][field]["is_hierarchical"]:
            def unpack_hierarchy(nodes, parent_code):
                """Serialize the node hierarchy by depth-first traversal.

                Yields: tuples of (code, parent_code)
                """
                for node in nodes:
                    if isinstance(node, dict):
                        next_parent_code, child_nodes = next(iter(node.items()))
                        # internal: unpack recursively
                        yield next_parent_code, parent_code
                        for deep_node, deep_parent in unpack_hierarchy(child_nodes,
                                next_parent_code):
                            yield (deep_node, deep_parent)
                    else:
                        # terminal: serialize
                        yield (node, parent_code)

            all_codes, parents = zip(*unpack_hierarchy(model["codings"][code]["display"], ""))
            dcols.update({
                "code": all_codes,
                "parent_code": parents,
                "meaning": [model["codings"][code]["codes_to_meanings"][c] for c in all_codes],
            })
        else:
            # No hierarchy; just unpack the codes dictionary
            codes, meanings = zip(*model["codings"][code]["codes_to_meanings"].items())
            dcols.update({"code": codes, "meaning": meanings})

        dcols["coding_name"] = [code] * len(dcols["code"])
        
        try:
            dframe = pd.DataFrame(dcols)
        except ValueError as exc:
            print({key: len(vals) for key, vals in dcols.items()},
                  file=sys.stderr)
            raise exc

        return dframe

    def load_entity_dictionary(self, descriptor):
        entity_dictionary = collections.OrderedDict()
        for entity_name in descriptor.model['entities']:
            entity = descriptor.model['entities'][entity_name]
            entity_dictionary[entity_name] = pd.DataFrame.from_dict([{
                "entity": entity_name,
                "entity_title": entity.get('entity_title'),
                "entity_label_singular": entity.get('entity_label_singular'),
                "entity_label_plural": entity.get('entity_label_plural'),
                "entity_description": entity.get('entity_description')
            }])
        return entity_dictionary

    def write(self, output_path="", sep=","):
        """Create CSV files with the contents of the dictionaries.
        """
        csv_opts = dict(
            sep=sep,
            header=True,
            index=False,
            na_rep="",
        )
        
        def as_dataframe(ord_dict_of_df):
            """Join all blocks into a pandas DataFrame."""
            df = pd.concat([b for b in ord_dict_of_df.values()], sort=False)
            return df

        coding_dframe = as_dataframe(self.coding_dictionary)
        output_file = os.path.join(output_path,"coding_dictionary.csv")
        coding_dframe.to_csv(output_file, **csv_opts)
        
        entity_dframe = as_dataframe(self.entity_dictionary)
        output_file = os.path.join(output_path,"entity_dictionary.csv")
        entity_dframe.to_csv(output_file, **csv_opts)