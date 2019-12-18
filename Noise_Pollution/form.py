from django import forms
from Noise_Pollution.models import Stanza
from django.forms import ModelChoiceField


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class NewSensor(forms.Form):
    room = MyModelChoiceField(queryset=Stanza.objects.all(), empty_label="- Select a Room -", label="Where is Located?")
    type = forms.TypedChoiceField(choices=(('', '- Select Sensor Type -'), ('analogical', 'Analogical'), ('digital', 'Digital')))
    email = forms.EmailField(label="Insert Email (Leave Blank for Rep's Email) :", required=False)


class MoveSensor(forms.Form):
    room = MyModelChoiceField(queryset=Stanza.objects.all(), empty_label="- Select a Room -", label="Where do you want move it?")


class NewRoom(forms.Form):
    name = forms.CharField(label="Room Name:", max_length=20, empty_value="ex. Office")
    rep = forms.CharField(label="Room Representative:", max_length=50, empty_value="Enter a Name")
    email = forms.EmailField(label="Insert Rep Email:")


class SetSensorTime(forms.Form):
    time = forms.TypedChoiceField(choices=(('0', '0s'), ('1', '1s'), ('2', '2s'), ('5', '5s')), label='')


class Filter(forms.Form):
    sensorType = forms.TypedChoiceField(choices=(('', '- All Sensors -'), ('0', 'Digital Sensors'), ('1', 'Analogical Sensors')), label='', required=False)
    room = MyModelChoiceField(queryset=Stanza.objects.all(), empty_label="- All Rooms -", label='', required=False)
