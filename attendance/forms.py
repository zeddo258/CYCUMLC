from django import forms

from .models import AttendanceRecord, Class, Student


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['student', 'course', 'date', 'arrival_time', 'remark']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize dropdown options to display meaningful labels
        self.fields['student'].queryset = Student.objects.all()
        self.fields['student'].label = "Student"
        self.fields['student'].widget.attrs.update({'class': 'form-control'})

        self.fields['course'].queryset = Class.objects.all()
        self.fields['course'].label = "Class"
        self.fields['course'].widget.attrs.update({'class': 'form-control'})

        self.fields['date'].label = "Date"
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
 
        self.fields['arrival_time'].label = "Arrival time"
        self.fields['arrival_time'].widget = forms.TimeInput(attrs={'type':'time', 'class':'form-control'})

        self.fields['remark'].label = "Remark (Optional)"
        self.fields['remark'].widget.attrs.update({'class': 'form-control'})

