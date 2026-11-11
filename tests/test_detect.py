import sys, unittest
from pathlib import Path
import cv2

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from detect import CLASS_NAMES, model_path, load_model, detect

class DetectorTest(unittest.TestCase):
    def test_model_and_classes(self):
        self.assertTrue(model_path().is_file())
        self.assertEqual(tuple(load_model().names.values()),CLASS_NAMES)
    def test_invalid_image_is_rejected(self):
        with self.assertRaises(ValueError): detect(None)
    def test_real_image_inference(self):
        image_path=next((ROOT/'dataset'/'ppe_3_classes_fixed'/'images'/'test').glob('*.*'))
        image=cv2.imread(str(image_path)); annotated,detections,elapsed=detect(image)
        self.assertEqual(annotated.shape,image.shape); self.assertGreater(elapsed,0); self.assertIsInstance(detections,list)

if __name__=='__main__': unittest.main()
