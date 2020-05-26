
lineEdit = """
        QLineEdit{
             background-color: white;
             border: 1 solid #ddd;
             border-radius: 5px;
             font: 12pt "Corbel";
             color: #43454f;
             padding:10px;
        }
        """

lineEdit_opt = """
        QLineEdit{
             background-color: #83a836;
             border: 2px solid #43454f;;
             border-radius: 5px;
             font: 12pt "Corbel";
             color: #fff;
             padding:10px;
        }
        """


lineEdit_warning = """
    QLineEdit{
         background-color: white;
         border: 1 solid #c00;
         border-radius: 5px;
         font: 12pt "Corbel";
         color: #43454f;
         padding:10px;
    }

"""
label_lineEdit = """
        QLabel{
            font-size: 23px;
            font: 12pt "Corbel";
            color: #43454f;
        }
        """
label_title = """
QLabel{
    text-align: center;
    font: 23pt "Corbel";
    color: #43454f;
}
"""

label_info_wrong = """
QLabel{
    text-align: center;
    font: 10pt "Corbel";
    color: #db0000;
}
"""

label_info_right = """
QLabel{
    text-align: center;
    font: 10pt "Corbel";
    color: #83a836;
}
"""

btn_radio = """
QRadioButton {
    font: 16pt 'Reem Kufi';
    font-size: 23px;
    font: 13pt 'Corbel';
    color:        #7b826b;
}
QRadioButton::indicator {
    background-color: #a8ad9e;
    width: 13px;
    height: 13px;
    border-radius: 11px;
    border: 5px solid #788f49;
}
QRadioButton::indicator:checked {
    background-color:		#43454f;
    border:                		5px solid #83a836;
    border-radius:         	11px;
}
QRadioButton:checked {
    color:      #83a836;
    border:        none;
}
QRadioButton::indicator:unchecked {
    background-color:    #7b826b;
    border: 5px solid #7b826b;
}
"""
btn_light = """
QPushButton{
    background-color:  #fff;
    border: 1 solid #83a836;
    border-radius: 20px;
    font: 13pt "Corbel";
    padding:6px;
    color: #83a836;
}
QPushButton:hover{
    background-color:  #aaa;
    border: 1 solid #ddd;
    color: #fff;
}
QPushButton:pressed{
    background-color:  #43454f;
    border: 1 solid #ddd;
    color: #fff;
}
"""

btn_dark = """
QPushButton{
    background-color:  #43454f;
    border: 1 solid #ddd;
    border-radius: 20px;
    font: 13pt "Corbel";
    padding:6px;
    color: #fff;
}
QPushButton:hover{
    background-color:  #aaa;
    border: 1 solid #ddd;
    color: #fff;
}
QPushButton:pressed{
    background-color:  #fff;
    border: 1 solid #83a836;
    color: #83a836;
}
"""

label_icon_name = """
QLabel{
    font-size: 20px;
    color: white;
    font: 16pt "Reem Kufi";
}
"""
frame_about = """
QFrame{
    margin: 0px;
    max-height:400px;
    max-width: 600px;
    background-color: #fff;
    border-radius: 20%;
}
"""
label_about_c = """
QLabel{
    margin: 0 40px 40px 40px;
    color: #555;
    font: 15pt "Corbel";
}
"""
label_about_name = """
QLabel{
    color: #43454f;
    font: 25pt "Reem Kufi";
}
"""

label_about_made = """
QLabel{
    color: #83a836;
    font: 15pt "Reem Kufi";
}
"""

label_about_version = """
QLabel{
    margin: 0 40px 40px 40px;
    padding-top: 30px;
    border-top: 1px solid #aaa;
    border-radius: none;
    color: #555;
    font: 15pt "Corbel";
}
"""
label_allegro_monitored_stat = """
QLabel{
    border: none;
    font-size: 23px;
    font: 10pt "Corbel";
    color: #43454f;
}
"""
label_allegro_monitored_name = """
QLabel{
    font: 75 12pt "Noto Serif Lao";
    border: none;
    font-size: 23px;
    font: 10pt "Corbel";
    font: 75 12pt "Noto Serif Lao";
    color: #43454f;
}
"""

label_allegro_monitored_link = """
QLabel{
    color: #fff;
    border: none;
    font: 14pt "Corbel";  
}
"""

main_window = """
 QScrollBar:vertical
 {
     background-color: #2A2929;
     width: 17px;
     margin: 15px 3px 15px 3px;
     border: 1px transparent #2A2929;
     border-radius: 5px;
 }

 QScrollBar::handle:vertical
 {
     background-color: #43454f;         /* #605F5F; */
     min-height: 5px;
     border-radius: 5px;
 }

 QScrollBar::sub-line:vertical
 {
     margin: 3px 0px 3px 0px;
     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);
     height: 10px;
     width: 10px;
     subcontrol-position: top;
     subcontrol-origin: margin;
 }

 QScrollBar::add-line:vertical
 {
     margin: 3px 0px 3px 0px;
     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);
     height: 10px;
     width: 10px;
     subcontrol-position: bottom;
     subcontrol-origin: margin;
 }

 QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
 {

     border-image: url(:/qss_icons/rc/up_arrow.png);
     height: 10px;
     width: 10px;
     subcontrol-position: top;
     subcontrol-origin: margin;
 }


 QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
 {
     border-image: url(:/qss_icons/rc/down_arrow.png);
     height: 10px;
     width: 10px;
     subcontrol-position: bottom;
     subcontrol-origin: margin;
 }

 QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
 {
     background: none;
 }


 QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
 {
     background: none;
 }


"""

btn_allegro_ops_auto = """
QPushButton{
    border:none;
    border-bottom: 1px solid #43454f;
    border-bottom: 1px solid #aaa;
    font: 13pt "Corbel";
    height: 70px;
    padding:6px;
    color: #83a836;
}
QPushButton:hover{
    background-color:  #aaa;
    color: #fff;
}
QPushButton:pressed{
    background-color:  #fff;
    color: #83a836;
}
QPushButton:checked {
    background-color:  #fff;
}
QPushButton:checked:hover {
    background-color:  #aaa;
    color: #fff;
}

QPushButton:checked:pressed{
    background-color:  #fff;
    color: #83a836;
}
"""

help_text = "Program jest używany do monitorowania stron internetowych\n" \
            "Dla dodania strony do monitorowania przejdź do kategorii 'Add' \n" \
            "i wypełnij wszystkie pola. Następnie masz dwie opcji:\n" \
            "\t1)po prostu monitorowanie\n" \
            "\t2)monitorowanie i kupowanie produktu\n" \
            "\nWszystkie twoje moniturujące strone można zobaczyć w kategorii 'Monitored'"
