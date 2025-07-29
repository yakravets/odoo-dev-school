from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class TestPatientVisit(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Visit = self.env['hr.hospital.patient.visit']
        self.Patient = self.env['hr.hospital.patient']
        self.Doctor = self.env['hr.hospital.doctor']
        self.Diagnosis = self.env['hr.hospital.medical.diagnosis']
        self.Currency = self.env['res.currency']

        self.patient = self.Patient.create({
            'name': 'Test Patient',
        })

        self.doctor = self.Doctor.create({
            'name': 'Dr. House',
            'license_number': 'ABC123',
        })

        self.currency = self.Currency.search([], limit=1)

    def test_create_visit(self):
        """Test basic creation of a patient visit"""
        visit = self.Visit.create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'planned_datetime': datetime.now() + timedelta(days=1),
            'status': 'planned',
            'visit_type': 'primary',
            'amount': 150.0,
            'currency_id': self.currency.id,
        })
        self.assertEqual(visit.status, 'planned')
        self.assertEqual(visit.visit_type, 'primary')
        self.assertEqual(visit.patient_id, self.patient)
        self.assertEqual(visit.doctor_id, self.doctor)
        self.assertEqual(visit.currency_id, self.currency)
        self.assertEqual(visit.amount, 150.0)
        self.assertTrue(visit.name.startswith('New') or visit.name)

    def test_diagnosis_count_computation(self):
        """Test computed field for diagnosis_count"""
        visit = self.Visit.create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'planned_datetime': datetime.now() + timedelta(days=1),
            'status': 'planned',
            'currency_id': self.currency.id,
        })

        diag1 = self.Diagnosis.create({
            'visit_id': visit.id,
            'name': 'Flu'
        })
        diag2 = self.Diagnosis.create({
            'visit_id': visit.id,
            'name': 'Cough'
        })

        visit.invalidate_recordset()
        self.assertEqual(visit.diagnosis_count, 2)

    def test_visit_types(self):
        """Test all visit types"""
        types = ['primary', 'repeat', 'preventive', 'emergency']
        for t in types:
            visit = self.Visit.create({
                'patient_id': self.patient.id,
                'doctor_id': self.doctor.id,
                'planned_datetime': datetime.now() + timedelta(days=1),
                'status': 'planned',
                'visit_type': t,
                'currency_id': self.currency.id,
            })
            self.assertEqual(visit.visit_type, t)

    def test_default_visit_unit(self):
        visit = self.Visit.create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'planned_datetime': datetime.now() + timedelta(days=1),
            'status': 'planned',
            'currency_id': self.currency.id,
        })
        self.assertEqual(visit.visit_unit, 1)
