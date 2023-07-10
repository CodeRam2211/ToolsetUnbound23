#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    unsigned char r;
    unsigned char g;
    unsigned char b;
    unsigned char a;
} Color;

int main() {
    const int imageWidth = 735;
    const int imageHeight = 588;
    const int channels = 4;

    Color prevColor = { 0, 0, 0, 255 };
    int run = 0;
    Color seenPixels[64] = { 0 };

    const int QOI_HEADER_SIZE = 14;
    unsigned char QOI_END_MARKER[] = { 0, 0, 0, 0, 0, 0, 0, 1 };
    const int QOI_END_MARKER_SIZE = sizeof(QOI_END_MARKER);

    FILE* file = fopen("a.ARW", "rb");
    if (!file) {
        printf("Failed to open raw image file.\n");
        return 1;
    }

    fseek(file, 0, SEEK_END);
    long imageSize = ftell(file);
    fseek(file, 0, SEEK_SET);

    int lastPixel = imageSize - channels;

    int maxSize = imageWidth * imageHeight * (channels + 1) + QOI_HEADER_SIZE + QOI_END_MARKER_SIZE;
    unsigned char* bytes = (unsigned char*)malloc(maxSize * sizeof(unsigned char));
    int index = 0;

    void write32(unsigned int value) {
        bytes[index++] = (value & 0xff000000) >> 24;
        bytes[index++] = (value & 0x00ff0000) >> 16;
        bytes[index++] = (value & 0x0000ff00) >> 8;
        bytes[index++] = (value & 0x000000ff) >> 0;
    }

    // Write the header
    write32(0x716f6966);
    write32(imageWidth);
    write32(imageHeight);
    bytes[index++] = channels;
    bytes[index++] = 1;

    unsigned char buffer[channels];
    for (int offset = 0; offset <= lastPixel; offset += channels) {
        fread(buffer, sizeof(unsigned char), channels, file);

        Color color = {
            .r = buffer[0],
            .g = buffer[1],
            .b = buffer[2],
            .a = (channels == 4) ? buffer[3] : prevColor.a
        };

        if (color.r == prevColor.r && color.g == prevColor.g && color.b == prevColor.b && color.a == prevColor.a) {
            run++;
            if (run == 62 || offset == lastPixel) {
                bytes[index++] = 0xc0 | (run - 1);
                run = 0;
            }
        }
        else {
            if (run > 0) {
                bytes[index++] = 0xc0 | (run - 1);
                run = 0;
            }

            unsigned char hash = (color.r * 3 + color.g * 5 + color.b * 7 + color.a * 11) % 64;
            if (color.r == seenPixels[hash].r && color.g == seenPixels[hash].g && color.b == seenPixels[hash].b && color.a == seenPixels[hash].a) {
                bytes[index++] = 0x00 | hash;
            }
            else {
                seenPixels[hash] = color;

                Color diff = {
                    .r = color.r - prevColor.r,
                    .g = color.g - prevColor.g,
                    .b = color.b - prevColor.b,
                    .a = color.a - prevColor.a
                };

                int dr_dg = diff.r - diff.g;
                int db_dg = diff.b - diff.g;

                if (diff.a == 0) {
                    if (diff.r >= -2 && diff.r <= 1 && diff.g >= -2 && diff.g <= 1 && diff.b >= -2 && diff.b <= 1) {
                        bytes[index++] = 0x40 | ((diff.r + 2) << 4) | ((diff.g + 2) << 2) | ((diff.b + 2) << 0);
                    }
                    else if (diff.g >= -32 && diff.g <= 31 && dr_dg >= -8 && dr_dg <= 7 && db_dg >= -8 && db_dg <= 7) {
                        bytes[index++] = 0x80 | (diff.g + 32);
                        bytes[index++] = ((dr_dg + 8) << 4) | (db_dg + 8);
                    }
                    else {
                        bytes[index++] = 0xfe;
                        bytes[index++] = color.r;
                        bytes[index++] = color.g;
                        bytes[index++] = color.b;
                    }
                }
                else {
                    bytes[index++] = 0xff;
                    bytes[index++] = color.r;
                    bytes[index++] = color.g;
                    bytes[index++] = color.b;
                    bytes[index++] = color.a;
                }
            }
        }

        prevColor = color;
    }

    for (int i = 0; i < QOI_END_MARKER_SIZE; i++) {
        bytes[index++] = QOI_END_MARKER[i];
    }

    fclose(file);

    FILE* output_file = fopen("encoded-c.qoi", "wb");
    if (!output_file) {
        printf("Failed to create output file.\n");
        free(bytes);
        return 1;
    }

    fwrite(bytes, sizeof(unsigned char), index, output_file);
    fclose(output_file);

    free(bytes);

    return 0;
}
