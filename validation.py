import cv2
from utils import _read_images

VAL_PATH = "validation\\"

class ValidateClass(object):

    def _load_validation(self,name):

        edge = "s"

        sup_l = []
        inf_l = []

        for line in open(VAL_PATH + name.split("\\")[1].split(".")[0] + '.txt', 'r'):
            if line.startswith("MARK"):
                edge = "i"
            elif edge == "s":
                sup_l.append((int(line.split("\t")[0]),int(line.split("\t")[1])))
            else:
                inf_l.append((int(line.split("\t")[0]), int(line.split("\t")[1])))

        return sup_l, inf_l

    def _show_validations(self, list_names, list_images):
        for i in range(0,len(list_names)):
            inf_l, sup_l  = self._load_validation(list_names[i])
            image = list_images[i]
            for i in range(1, len(inf_l)):
                cv2.line(image, inf_l[i - 1], inf_l[i], (0, 255, 0))
            for i in range(1, len(sup_l)):
                cv2.line(image, sup_l[i - 1], sup_l[i], (255, 255, 0))
            cv2.imshow("aoi_window", image)
            cv2.waitKey()

    def _validate(self, images_list, names_list):

        for i in range(0,len(images_list)):
            self._create_contour_validation(images_list[i],names_list[i])

    def _create_contour_validation(self, image, name):
        aoi_params = dict(line = 's', points_s=[], points_i = [], image=image)

        cv2.namedWindow("aoi_window")
        cv2.setMouseCallback("aoi_window", self._on_mouse_clicked_aoi, aoi_params)
        stop = False

        while not stop:
            cv2.imshow("aoi_window", image)
            k = cv2.waitKey() & 0xff
            if (k == ord('\n') or k == ord(' ')) and aoi_params["line"]=='s':
                aoi_params["line"] = 'i'
                l_sup = list(aoi_params["points_s"])
                for i in range(1, len(l_sup)):
                    cv2.line(image, l_sup[i - 1], l_sup[i], (255, 255, 0))
            elif k == ord('\n') or k == ord(' '):
                stop = True
            elif k == ord("d") or k == ord("D"):

                if len(list(aoi_params["points_"+aoi_params["line"]]))>0:
                    aoi_params["points_"+aoi_params["line"]] = aoi_params["points_"+aoi_params["line"]][:-1]

                l_sup = list(aoi_params["points_s"])
                for i in range(1, len(l_sup)):
                    cv2.line(image, l_sup[i - 1], l_sup[i], (255, 255, 0))

                if aoi_params["line"] == "i":
                    l_inf = list(aoi_params["points_i"])
                    for i in range(1, len(l_inf)):
                        cv2.line(image, l_inf[i - 1], l_inf[i], (0, 255, 0))

        s_list = list(aoi_params["points_s"])
        i_list = list(aoi_params["points_i"])

        output  = ""
        for x,y in s_list:
            output += str(x) + "\t" + str(y) + "\n"
        output += "MARK\n"
        for x,y in i_list:
            output += str(x) + "\t" + str(y) + "\n"

        with open(VAL_PATH + name.split("\\")[1].split(".")[0] + '.txt', 'w') as file:
            file.write(output)
            file.close()

    def _on_mouse_clicked_aoi(self, event, x, y, flags, aoi_params):

        img_copy = aoi_params["image"] * 1

        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(img_copy, (x, y), 3, (0, 255, 255), 2)

        elif event == cv2.EVENT_LBUTTONUP:
            l = list(aoi_params["points_"+aoi_params["line"]])
            l.append((x, y))
            aoi_params["points_"+aoi_params["line"]] = l

        l_inf = list(aoi_params["points_i"])
        for i in range(1, len(l_inf)):
            cv2.line(img_copy, l_inf[i - 1], l_inf[i], (0, 255, 0))

        l_sup = list(aoi_params["points_s"])
        for i in range(1,len(l_sup)):
            cv2.line(img_copy, l_sup[i-1], l_sup[i], (255, 255, 0))

        cv2.imshow("aoi_window", img_copy)

    def create_validation(self):

        image_list, names_list = _read_images()

        self._validate(image_list,names_list)