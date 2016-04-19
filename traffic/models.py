from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
import datetime as dt


class Agency(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()


class Violation(models.Model):
    id = models.CharField(max_length=24, primary_key=True)
    description = models.TextField()

    def __str__(self):
        return "{} ({})".format(self.id, self.description)


TICKET_TYPES = (
    ("photo", "Photo"),
    ("moving", "Moving"),
    ("mover void", "Mover Void"),
    ("no ticket type", "No Ticket Type"),
)


class Moving(models.Model):
    id = models.IntegerField(primary_key=True)
    location = models.PointField()

    fine_amount = models.IntegerField()
    paid_amount = models.IntegerField()

    location_name = models.TextField()
    when = models.DateField()

    agency = models.ForeignKey(Agency)
    violation = models.ForeignKey(Violation)

    type = models.CharField(max_length=16, choices=TICKET_TYPES)
    accident = models.BooleanField()

    @classmethod
    def create_from_csv(self, obj):
        # {'ADDRESS_ID': '806823',
        #  'PENALTY1': '', 
        #  'ACCIDENTINDICATOR': 'No',
        #  'PENALTY2': '',
        id = int(obj.get('ROW_', obj.get('ROWID_')))
        # Check to see if this is really unique

        agency_id = int(obj['AGENCYID'])
        try:
            agency = Agency.objects.get(id=agency_id)
        except Agency.DoesNotExist:
            agency = Agency.objects.create(id=agency_id)

        violation_id = obj['VIOLATIONCODE']
        try:
            violation = Violation.objects.get(id=violation_id)
        except Violation.DoesNotExist:
            violation = Violation.objects.create(
                id=violation_id,
                description=obj['VIOLATIONDESC'],
            )

        when = dt.datetime.strptime(
            obj['TICKETISSUEDATE'],
            "%Y-%m-%dT00:00:00.000Z",
        )

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
            paid_amount=int(obj['TOTALPAID']),
            location_name=obj['LOCATION'],
            when=when,
            agency=agency,
            violation=violation,
            type=obj['TICKETTYPE'].lower(),
            accident={
                "No": False,
                "Yes": True,
            }[obj['ACCIDENTINDICATOR']]
        )
