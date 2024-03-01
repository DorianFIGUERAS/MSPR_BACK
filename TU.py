import json
import unittest
from unittest.mock import patch, MagicMock, Mock
from app import app  # Make sure to import your Flask app here
from descriptif import descriptif_table
from prediction import modele
from table_user import table_user_id
from upload_BDD import upload_on_bdd

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_receive_uid(self):
        response = self.app.post('/userid', json={'uid': '12345'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('UID reçu avec succès', data['message '])
        self.assertEqual(data['uid '], '12345')

    @patch('app.modele')
    @patch('app.upload_on_bdd')
    @patch('app.descriptif_table')
    def test_upload_photo(self, mock_descriptif_table, mock_upload_on_bdd, mock_modele):
        mock_modele.return_value = ('dog', 95)
        mock_upload_on_bdd.return_value = True
        mock_descriptif_table.return_value = ('details about dog', 'http://image.url')
        
        with open('Dog-Tracks-5.jpg', 'rb') as img:
            response = self.app.post('/upload_photo', data={'photo': img}, content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('Informations ', data)
        self.assertIn('pourcentage ', data)
        self.assertIn('url ', data)

    @patch('app.firestore.client')
    def test_get_table_user(self, mock_client):
        # Here you would mock firestore client behavior and responses
        pass

class TestDescriptifTable(unittest.TestCase):

    @patch('app.firestore.client')
    @patch('app.firebase_admin.initialize_app')
    def test_descriptif_table_success(self, mock_initialize, mock_client):
        # Mock Firestore document references and their return values
        doc_snapshot = MagicMock()
        doc_snapshot.exists = True
        doc_snapshot.to_dict.return_value = {
            "descriptif_famille": "Mammifères",
            "descriptif_description": "Petit mammifère aquatique",
            "descriptif_taille": "50 cm",
            "descriptif_habitat": "Rivières",
            "descriptif_espece": "Castor",
            "descriptif_region": "Europe"
        }

        image_doc_snapshot = MagicMock()
        image_doc_snapshot.exists = True
        image_doc_snapshot.to_dict.return_value = {
            "animal_imageurl": "http://example.com/image.jpg"
        }

        mock_client.return_value.collection.return_value.document.return_value.get.side_effect = [doc_snapshot, image_doc_snapshot]

        prediction = "castor"
        valeurs, image_url = descriptif_table(prediction)

        self.assertIn("Mammifères", valeurs)
        self.assertIn("http://example.com/image.jpg", image_url)

    @patch('app.firestore.client')
    @patch('app.firebase_admin.initialize_app')
    def test_descriptif_table_no_document(self, mock_initialize, mock_client):
        # Mock Firestore document references to simulate non-existing documents
        doc_snapshot = MagicMock()
        doc_snapshot.exists = False

        image_doc_snapshot = MagicMock()
        image_doc_snapshot.exists = False

        mock_client.return_value.collection.return_value.document.return_value.get.side_effect = [doc_snapshot, image_doc_snapshot]

        prediction = "chat"
        result = descriptif_table(prediction)

        self.assertIsInstance(result, str)
        self.assertTrue("Aucun document trouvé" in result)

# class TestModeleFunction(unittest.TestCase):

#     @patch('prediction.tf.keras.models.load_model')
#     @patch('prediction.json.load')
#     @patch('prediction.tf.keras.preprocessing.image.load_img')
#     @patch('prediction.tf.keras.preprocessing.image.img_to_array')
#     @patch('prediction.tf.expand_dims')
#     @patch('prediction.np.argmax')
#     def test_modele(self, mock_argmax, mock_expand_dims, mock_img_to_array, mock_load_img, mock_json_load, mock_load_model):
#         # Setup mock behavior
#         mock_json_load.return_value = {0: 'castor', 1: 'chat'}
#         mock_load_img.return_value = 'image_mock'
#         mock_img_to_array.return_value = 'image_array_mock'
#         mock_expand_dims.return_value = 'expanded_image_array_mock'
#         mock_argmax.return_value = 1  # Simulating that the prediction is 'dog'
#         mock_model = MagicMock()
#         mock_load_model.return_value = mock_model
#         mock_model.predict.return_value = [[0.2, 0.8]]  # Mock prediction result
        
#         # Call the function under test
#         predicted_class = modele('Dog-Tracks-5.jpg')
        
#         # Assertions
#         mock_load_model.assert_called_once_with('IA')
#         mock_load_img.assert_called_once()
#         mock_img_to_array.assert_called_once_with('image_mock')
#         mock_expand_dims.assert_called_once()
#         mock_model.predict.assert_called_once()
#         mock_argmax.assert_called_once()
#         self.assertEqual(predicted_class, 'dog')

class TestTableUserIdFunction(unittest.TestCase):

    @patch('table_user.firebase_admin.initialize_app')
    @patch('table_user.firestore.client')
    def test_table_user_id(self, mock_client, mock_initialize_app):
        # Mock Firestore document snapshots
        doc_snapshot_1 = MagicMock()
        doc_snapshot_1.to_dict.return_value = {'url_image': 'http://example.com/image1.jpg', 'prediction': 'cat'}
        
        doc_snapshot_2 = MagicMock()
        doc_snapshot_2.to_dict.return_value = {'url_image': 'http://example.com/image2.jpg', 'prediction': 'dog'}
        
        # Mock Firestore query
        mock_query = MagicMock()
        mock_query.stream.return_value = [doc_snapshot_1, doc_snapshot_2]
        mock_client.return_value.collection.return_value.where.return_value = mock_query

        # Expected JSON result
        expected_json = json.dumps([
            {'url_image': 'http://example.com/image1.jpg', 'prediction': 'cat'},
            {'url_image': 'http://example.com/image2.jpg', 'prediction': 'dog'}
        ])

        # Call the function under test
        user_id = 'test_user_id'
        result_json = table_user_id(user_id)
        
        # Assertions
        mock_client.assert_called_once()  # Ensure Firestore client is called
        mock_query.stream.assert_called_once()  # Ensure the query is executed
        self.assertEqual(result_json, expected_json)

class TestUploadOnBddFunction(unittest.TestCase):

    @patch.dict('upload_BDD.firebase_admin._apps', {}, clear=True)
    @patch('upload_BDD.firebase_admin.get_app')
    @patch('upload_BDD.firebase_admin.initialize_app')
    @patch('upload_BDD.storage.bucket')
    @patch('upload_BDD.firestore.client')
    def test_upload_on_bdd(self, mock_firestore_client, mock_storage_bucket, mock_initialize_app, mock_get_app):
        mock_app = Mock()
        mock_initialize_app.return_value = mock_app
        mock_get_app.return_value = mock_app

        # Mocking Firebase Storage upload
        mock_bucket = Mock()
        mock_storage_bucket.return_value = mock_bucket
        mock_blob = Mock()
        mock_bucket.blob.return_value = mock_blob
        mock_blob.public_url = 'http://example.com/uploaded_image.jpg'

        # Mocking Firestore document update
        mock_db = Mock()
        mock_firestore_client.return_value = mock_db
        mock_doc_ref = Mock()
        mock_db.collection.return_value.document.return_value = mock_doc_ref

        # Execute the function with test data
        image_path = 'test_image.jpg'
        useruid = 'test_user'
        prediction = 'test_prediction'
        result = upload_on_bdd(image_path, useruid, prediction)

        # Assertions to verify the expected behavior
        mock_initialize_app.assert_called_once()
        mock_storage_bucket.assert_called_once_with('footprints-8e343.appspot.com', app=mock_app)
        mock_bucket.blob.assert_called_once_with(f"images_user/{image_path}USER{useruid}")
        mock_blob.upload_from_filename.assert_called_once_with(image_path)
        mock_blob.make_public.assert_called_once()
        mock_db.collection.assert_called_once_with('images_user')
        mock_doc_ref.set.assert_called_once_with({
            'url_image': 'http://example.com/uploaded_image.jpg',
            'user_id': useruid,
            'prediction': prediction
        })
        self.assertEqual(result, "Merci pour votre contribution à WildLens ! ")


if __name__ == '__main__':
    unittest.main()
