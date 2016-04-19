from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry


class Moving(models.Model):
    id = models.IntegerField(primary_key=True)
    location = models.PointField()

    fine_amount = models.IntegerField()
    location_name = models.TextField()

    @classmethod
    def create_from_csv(self, obj):
        # {'OBJECTID': '1090162', 'Y': '38.905030892799999', 'LOCATION': 'M ST W/B @ WHITEHURST FWY NW', 'ADDRESS_ID': '806823', 'FINEAMT': '150', 'ROW_': '2755995', 'PENALTY1': '', '\ufeffX': '-77.070231129299998', 'YCOORD': '137465.2499', 'VIOLATIONCODE': 'T113', 'TICKETISSUEDATE': '2012-11-01T00:00:00.000Z', 'TOTALPAID': '150', 'VIOLATIONDESC': 'FAIL TO STOP PER REGULATIONS FACING RED SIGNAL', 'XCOORD': '393908.51', 'TICKETTYPE': 'Photo', 'ACCIDENTINDICATOR': 'No', 'ROW_ID': '', 'PENALTY2': '', 'STREETSEGID': '5856', 'AGENCYID': '25'}
        id = int(obj.get('ROW_', obj.get('ROWID_')))
        # Check to see if this is really unique

        try:
            moving = Moving.objects.get(id=id)
            # For now, let's remove anything that we touched before.
            moving.delete()
        except Moving.DoesNotExist:
            pass

        if '\ufeffX' in obj:
            obj['X'] = obj['\ufeffX']

        coords = GEOSGeometry('POINT({lon} {lat})'.format(
            lat=obj['X'],
            lon=obj['Y'],
        ))

        return Moving.objects.create(
            id=id,
            location=coords,
            fine_amount=int(obj['FINEAMT']) if obj['FINEAMT'] else 0,
            location_name=obj['LOCATION'],
        )
