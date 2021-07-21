from ..models.location import Provincials, Districts, Wards
import json


def add_location():
    print("start")
    with open("media/local.json") as f:
        data = json.load(f)
        for p in data:
            print("pro")
            pro = Provincials.objects.filter(code=p['code'])
            if not pro:
                print("d")
                provincal = Provincials.objects.create(
                    code=p['code'],
                    name=p['name']
                )
                for d in p['districts']:
                    district = Districts.objects.create(
                        name=d['name'],
                        provincial=provincal
                    )
                    for w in d["wards"]:
                        ward = Wards.objects.create(
                            name=w['name'],
                            prefix=w['prefix'],
                            district=district
                        )
                        ward.save()
                    for w in d["streets"]:
                        ward = Wards.objects.create(
                            name=w['name'],
                            prefix=w['prefix'],
                            district=district
                        )
                        ward.save()
                    district.save()
                provincal.save()
    print("end")

