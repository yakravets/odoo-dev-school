from odoo.tests.common import TransactionCase


class TestTypeOfDisease(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Disease = self.env['hr.hospital.type.of.disease']

    def test_create_basic_disease(self):
        """Test creation of a simple disease"""
        disease = self.Disease.create({
            'name': 'Influenza',
            'severity': 'moderate',
        })
        self.assertEqual(disease.name, 'Influenza')
        self.assertEqual(disease.severity, 'moderate')
        self.assertTrue(disease.active)

    def test_required_fields(self):
        """Test missing required field severity"""
        with self.assertRaises(Exception):
            self.Disease.create({'name': 'Nameless Disease'})

    def test_severity_and_danger_levels(self):
        """Test all possible severity/danger level values"""
        for severity in ['mild', 'moderate', 'severe', 'critical']:
            d = self.Disease.create({
                'name': f'Disease {severity}',
                'severity': severity,
            })
            self.assertEqual(d.severity, severity)

        disease = self.Disease.create({
            'name': 'Test Danger',
            'severity': 'severe',
            'danger_level': 'high',
        })
        self.assertEqual(disease.danger_level, 'high')

    def test_contagious_flag(self):
        """Test contagious boolean flag"""
        disease = self.Disease.create({
            'name': 'COVID-19',
            'severity': 'critical',
            'is_contagious': True
        })
        self.assertTrue(disease.is_contagious)

    def test_icd10_code_length(self):
        """Test ICD-10 code length (optional field)"""
        disease = self.Disease.create({
            'name': 'Diabetes',
            'severity': 'moderate',
            'icd10_code': 'E11'
        })
        self.assertEqual(disease.icd10_code, 'E11')

    def test_parent_child_relationship(self):
        """Test recursive relationship between diseases"""
        parent = self.Disease.create({
            'name': 'Respiratory Diseases',
            'severity': 'mild',
        })
        child = self.Disease.create({
            'name': 'Asthma',
            'severity': 'moderate',
            'parent_id': parent.id,
        })
        self.assertEqual(child.parent_id, parent)
        self.assertIn(child, parent.child_ids)

    def test_region_distribution(self):
        """Test M2M relationship with res.country"""
        country_model = self.env['res.country']
        ukraine = country_model.search([('code', '=', 'UA')], limit=1)
        poland = country_model.search([('code', '=', 'PL')], limit=1)

        disease = self.Disease.create({
            'name': 'Tuberculosis',
            'severity': 'severe',
            'region_ids': [(6, 0, [ukraine.id, poland.id])]
        })

        self.assertIn(ukraine, disease.region_ids)
        self.assertIn(poland, disease.region_ids)
