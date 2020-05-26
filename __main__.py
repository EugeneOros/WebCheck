import sys
# import ui.stylesheet
import monitoring
import multiprocessing
import ui.gui


def main(shared_dict):
    app = ui.gui.QApplication(sys.argv)
    win = ui.gui.MainWindow(shared_dict)
    win.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        shared_dict = manager.dict({'isTerminatedP2': False})
        p1 = multiprocessing.Process(target=main, args=[shared_dict])
        p2 = multiprocessing.Process(target=monitoring.start_monitor, args=[shared_dict])
        p1.start()
        p2.start()
        p2.join()
        p1.join()
        # while True:
        #     if shared_dict['isTerminatedP2']:
        #         print(shared_dict['isTerminatedP2'])
        #         p2.terminate()
        #         break

