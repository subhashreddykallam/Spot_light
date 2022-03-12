import tensorflow as tf
import cv2
import numpy as np
import os
class super_resolution:
    def __init__(self, config, scale):
        self.config = config
        self.scale = scale
        fileDir = os.path.realpath(__file__)
        ckpt = os.path.join(fileDir, '../CKPT_dir/x{}_small'.format(self.scale))
        self.ckpt_path = os.path.abspath(os.path.realpath(ckpt))

    def upscale(self, img):
        """
        Upscales an image via model.
        """
        img_ycc = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        img_y = img_ycc[:,:,0]
        floatimg = img_y.astype(np.float32) / 255.0
        LR_input_ = floatimg.reshape(1, floatimg.shape[0], floatimg.shape[1], 1)
        output = []
        with tf.compat.v1.Session(config=self.config) as sess:
            # load and run
            ckpt_name = self.ckpt_path + "/fsrcnn_ckpt" + ".meta"
            saver = tf.compat.v1.train.import_meta_graph(ckpt_name)
            saver.restore(sess, tf.train.latest_checkpoint(self.ckpt_path))
            graph_def = sess.graph
            LR_tensor = graph_def.get_tensor_by_name("IteratorGetNext:0")
            HR_tensor = graph_def.get_tensor_by_name("NHWC_output:0")

            output = sess.run(HR_tensor, feed_dict={LR_tensor: LR_input_})

            # post-process
            Y = output[0]
            Y = (Y * 255.0).clip(min=0, max=255)
            Y = (Y).astype(np.uint8)

            # Merge with Chrominance channels Cr/Cb
            Cr = np.expand_dims(cv2.resize(img_ycc[:,:,1], None, fx=self.scale, fy=self.scale, interpolation=cv2.INTER_CUBIC), axis=2)
            Cb = np.expand_dims(cv2.resize(img_ycc[:,:,2], None, fx=self.scale, fy=self.scale, interpolation=cv2.INTER_CUBIC), axis=2)
            output = (cv2.cvtColor(np.concatenate((Y, Cr, Cb), axis=2), cv2.COLOR_YCrCb2BGR))
        sess.close()
        return output
