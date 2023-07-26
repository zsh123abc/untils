import os
import cv2
import numpy as np
import paddle
import yaml

from object_detect import ObjectDetect

from paddle_deploy.infer import Detector, DetectorPicoDet, PredictConfig, print_arguments, get_test_images, bench_log

from tools import distance, getBoxCenterCoord

class ObjectDetectBasketballCourtPaddle(ObjectDetect):
    
    def __init__(self, confidence_threshold=0.5, device='GPU'):
        super(__class__,self).__init__(confidence_threshold)
        
        #根据模型定义修改
        self.CLASS_ID_F_COURT = 1
        self.CLASS_ID_T_COURT = 0

        self.device = device
        #self.det_model_dir = './models/ppyoloe_plus_sod_crn_l_80e_coco_basketball_aug/'
        #self.det_model_dir = './models/picodet_s_320_coco_lcnet_basketball_only_0.859_aug_0416/'
        self.det_model_dir = '/data2/PaddleDetection2.6/inference_model/outside_court/'
        deploy_file = os.path.join(self.det_model_dir, 'infer_cfg.yml')
        with open(deploy_file) as f:
            yml_conf = yaml.safe_load(f)
        arch = yml_conf['arch']
        detector_func = 'Detector'
        if arch == 'PicoDet':
            detector_func = 'DetectorPicoDet'

        self.run_mode='paddle'
        self.trt_min_shape=1
        self.trt_max_shape=1280
        self.trt_opt_shape=640
        self.trt_calib_mode=False
        self.cpu_threads=1
        self.enable_mkldnn=False

        self.detector = eval(detector_func)(self.det_model_dir,
                                   device=self.device,
                                   run_mode=self.run_mode,
                                   trt_min_shape=self.trt_min_shape,
                                   trt_max_shape=self.trt_max_shape,
                                   trt_opt_shape=self.trt_opt_shape,
                                   trt_calib_mode=self.trt_calib_mode,
                                   cpu_threads=self.cpu_threads,
                                   enable_mkldnn=self.enable_mkldnn,
                                   threshold=self.confidence_threshold)
        

    def sort_boxes_by_cls_conf(self, objBoxes):
        #cls, conf, x1, y1, x2, y2 = box
        return sorted(objBoxes, key=lambda x: (x[0], x[1]))
    
    def detect(self, frame, width, height):
        if type(frame) is str:
            img = cv2.imread(frame)
            height, width, _ = img.shape
        else:
            img = frame.copy()

        detect_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        results = self.detector.predict_image([detect_frame], visual=False) #, slice_size=[320, 320])
        results = self.detector.filter_box(results, self.confidence_threshold)
        
        boxes_ = []
        
        if results['boxes_num'] > 0:
            for i, box in enumerate(results["boxes"]):
                cls, conf, x1, y1, x2, y2 = box
                cls = int(cls)

                boxes_.append([cls, conf, x1, y1, x2, y2])

        return self.sort_boxes_by_cls_conf(boxes_)
