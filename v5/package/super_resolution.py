import tensorflow as tf
import cv2
import numpy as np
import os
class super_resolution:
    def __init__(self, config, scale):
        self.config = config
        self.scale = scale
        fileDir = os.path.realpath(__file__)
        ckpt = os.path.join(fileDir, '../models/FSRCNN-small_x{}.pb'.format(self.scale))
        self.pbPath = os.path.abspath(os.path.realpath(ckpt))

    def load_pb(self, path_to_pb):
        with tf.io.gfile.GFile(path_to_pb, "rb") as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())
        with tf.Graph().as_default() as graph:
            tf.import_graph_def(graph_def, name='')
            return graph

    def upscale(self, fullimg):
        # Get graph
        out = []
        graph = self.load_pb(self.pbPath)

        width = fullimg.shape[0]
        height = fullimg.shape[1]

        img = fullimg[0:(width - (width % self.scale)), 0:(height - (height % self.scale)), :]
        # img = cv2.resize(cropped, None, fx=self.scale, fy=self.scale, interpolation=cv2.INTER_CUBIC)
        # cv2.imshow("img", img)

        # to ycrcb and normalize
        img_ycc = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        img_y = img_ycc[:,:,0]
        floatimg = img_y.astype(np.float32) / 255.0

        LR_input_ = floatimg.reshape(1, floatimg.shape[0], floatimg.shape[1], 1)

        LR_tensor = graph.get_tensor_by_name("IteratorGetNext:0")
        HR_tensor = graph.get_tensor_by_name("NHWC_output:0")

        with tf.compat.v1.Session(graph=graph) as sess:
            output = sess.run(HR_tensor, feed_dict={LR_tensor: LR_input_})

            # post-process
            Y = output[0]
            Y = (Y * 255.0).clip(min=0, max=255)
            Y = (Y).astype(np.uint8)

            # Merge with Chrominance channels Cr/Cb
            Cr = np.expand_dims(cv2.resize(img_ycc[:,:,1], None, fx=self.scale, fy=self.scale, interpolation=cv2.INTER_CUBIC), axis=2)
            Cb = np.expand_dims(cv2.resize(img_ycc[:,:,2], None, fx=self.scale, fy=self.scale, interpolation=cv2.INTER_CUBIC), axis=2)
            out = (cv2.cvtColor(np.concatenate((Y, Cr, Cb), axis=2), cv2.COLOR_YCrCb2BGR))

        sess.close()
        return out