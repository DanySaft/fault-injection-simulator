// target.c
int verify_acces(int input) {
    int expected_token = 0x1337;
    int is_valid = 0;

    if (input == expected_token) {
        is_valid = 1;
    }

    return is_valid;
}
