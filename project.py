import re
import json
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'projects.txt')

class Project:
    project_details = {
        "data": {
            "monument_id": 0,
            "site_name": "",
            "thumbnail": "",
            "latitude": 0,
            "longitude": 0,
            "category": "",
            "states": "",
            "criteria": "",
            "danger": "",
            "inscribed_date": 0,
            "extension": 0,
            "historical_description": "",
            "site_url": "https://geobrugg.com",
            "justification": "",
            "location_description": "Location description",
            "long_descsription": "<p>Situation</p>",
            "region": "",
            "revision": 0,
            "short_description": "",
            "transboundary": 0,
            "unique_number": 4,
            "isoCode": "",
            "secondary_dates": 2001
        }
    }
    amount_pics = 0

    pics = {
        "data": []
    }

    #constructor with no. of pics and project name
    def __init__(self, data_dict):
        self.data = []
        self.amount_pics = data_dict["pics"]
        self.project_details["data"]["transboundary"] = data_dict["pics"]
        self.project_details["data"]["site_name"] = data_dict["name"]
        self.project_details["data"]["latitude"] = data_dict["lat"]
        self.project_details["data"]["longitude"] = data_dict["lon"]
        self.project_details["data"]["states"] = data_dict["state"]
        self.project_details["data"]["criteria"] = data_dict["product"]
        self.project_details["data"]["inscribed_date"] = data_dict["year"]
        self.project_details["data"]["short_description"] = data_dict["desc"]
        self.project_details["data"]["category"] = data_dict["category"]
        self.pics["data"] = list()
        x = 0
        for x in range(self.amount_pics):
            self.pics["data"].append({
                "picture_id": x + 1,
                "approved": 1,
                "picture_url": "",
                "monument_id": self.project_details["data"]["monument_id"]
                })


    def create_txt_file(self):
        self.file_name = "project" + str(self.project_details["data"]["monument_id"]) + ".txt"
        self.path_data = "static/projectdetails/" + self.file_name
        self.path_pic = "static/projectpictures/pics" + self.file_name
        complete_path_data = os.path.join(THIS_FOLDER, self.path_data)
        complete_path_pic = os.path.join(THIS_FOLDER, self.path_pic)
        text_file = open(complete_path_data, "w")
        text_file.write(json.dumps(self.project_details))
        text_file.close()
        pic_file = open(complete_path_pic, "w")
        pic_file.write(json.dumps(self.pics))
        pic_file.close()

    def converted_project(self):
        conv = {
            "monument_id": self.project_details["data"]["monument_id"],
            "latitude": self.project_details["data"]["latitude"],
            "longitude": self.project_details["data"]["longitude"],
            "thumbnail": self.project_details["data"]["thumbnail"],
            "site_name": self.project_details["data"]["site_name"],
            "category": self.project_details["data"]["category"],
            "states": self.project_details["data"]["states"],
            "inscribed_date": self.project_details["data"]["inscribed_date"],
            "criteria": self.project_details["data"]["criteria"]
        }
        return(conv)

    def set_thumbnail(self, url):
        url_pattern = re.compile(r"""(?xi)
            \b
            (							# Capture 1: entire matched URL
                (?:
                https?:				# URL protocol and colon
                (?:
                /{1,3}						# 1-3 slashes
                |								#   or
                [a-z0-9%]						# Single letter or digit or '%'
         	    							# (Trying not to match e.g. "URI::Escape")
                )
                |							#   or
    		    					# looks like domain name followed by a slash:
                [a-z0-9.\-]+[.]
                (?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj| Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)
                /
                )
                (?:							# One or more:
                [^\s()<>{}\[\]]+						# Run of non-space, non-()<>{}[]
                |								#   or
                \([^\s()]*?\([^\s()]+\)[^\s()]*?\)  # balanced parens, one level deep: (…(…)…)
                |
                \([^\s]+?\)							# balanced parens, non-recursive: (…)
                )+
                (?:							# End with:
                \([^\s()]*?\([^\s()]+\)[^\s()]*?\)  # balanced parens, one level deep: (…(…)…)
                |
                \([^\s]+?\)							# balanced parens, non-recursive: (…)
                |									#   or
                [^\s`!()\[\]{};:'".,<>?«»“”‘’]		# not a space or one of these punct chars
                )
                |					# OR, the following to match naked domains:
                (?:
  	            (?<!@)			# not preceded by a @, avoid matching foo@_gmail.com_
                [a-z0-9]+
                (?:[.\-][a-z0-9]+)*
                [.]
                (?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj| Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)
                \b
                /?
                (?!@)			# not succeeded by a @, avoid matching "foo.na" in "foo.na@example.com"
                )
            )""")
        if re.match(url_pattern, url):
            self.project_details["data"]["thumbnail"] = url
        else:
            print("Not a valid URL")

    def set_iso(self, iso):
        self.project_details["data"]["isoCode"] = iso

