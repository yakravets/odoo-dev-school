from odoo.tests.common import TransactionCase


class TestSpecialization(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Specialization = self.env['hr.hospital.specialization']

    def test_create_specialization(self):
        """Test creation of specialization with required fields"""
        spec = self.Specialization.create({
            'name': 'Cardiology',
            'code': 'CARD',
            'description': 'Heart related specialization'
        })

        self.assertEqual(spec.name, 'Cardiology')
        self.assertEqual(spec.code, 'CARD')
        self.assertTrue(spec.active)

    def test_required_fields(self):
        """Test that name and code are required"""
        with self.assertRaises(Exception):
            self.Specialization.create({
                'description': 'Missing required fields'
            })

    def test_code_max_length(self):
        """Test that code does not exceed 10 characters"""
        with self.assertRaises(Exception):
            self.Specialization.create({
                'name': 'Neurology',
                'code': 'TOO_LONG_CODE_123',
            })

    def test_doctor_relation(self):
        """Test relation to doctors"""
        doctor_model = self.env['hr.hospital.doctor']

        spec = self.Specialization.create({
            'name': 'Dermatology',
            'code': 'DERM',
        })

        doctor = doctor_model.create({
            'name': 'Dr. House',
            'specialization_id': spec.id,
        })

        self.assertIn(doctor, spec.doctor_ids)
