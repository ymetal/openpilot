const int touch_timeout = 25;

typedef struct UICstmButton {
    char btn_name[6];
    char btn_label[6];
    char btn_label2[11];
} UICstmButton;

typedef struct BBUIState {
    int touch_last_x;
    int touch_last_y;
    bool touch_last;
    int touch_timeout;
    int touch_last_width;
    bool shouldDrawFrame;
    UICstmButton btns[6];
    char btns_status[6];
    char car_model[40];
    char car_folder[20];
    zsock_t *uiButtonInfo_sock;
    void *uiButtonInfo_sock_raw;
    zsock_t *uiCustomAlert_sock;
    void *uiCustomAlert_sock_raw;
    zsock_t *uiSetCar_sock;
    void *uiSetCar_sock_raw;
    zsock_t *uiPlaySound_sock;
    void *uiPlaySound_sock_raw;
    zsock_t *uiButtonStatus_sock;
    void *uiButtonStatus_sock_raw; 
    zsock_t *gps_sock;
    void *gps_sock_raw;
    int btns_x[6];
    int btns_y[6];
    int btns_r[6];
    int custom_message_status;
    char custom_message[120];
    int img_logo;
    int img_logo2;
    int img_logo_times;
    int img_car;
    int tri_state_switch;
    long tri_state_switch_last_read;
    uint16_t maxCpuTemp;
    uint32_t maxBatTemp;
    float gpsAccuracy ;
    float freeSpace;
    float angleSteers;
    float angleSteersDes;
} BBUIState;
