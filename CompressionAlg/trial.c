#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

struct color{
    int r;
    int g;
    int b;
    int a;
};

int QOI_HEADER_SIZE = 14;
int QOI_END_MARKER[] = {0, 0, 0, 0, 0, 0, 0, 1};
int QOI_END_MARKER_SIZE = sizeof(QOI_END_MARKER)/sizeof(int);

int QOI_OP_RUN   = 0xc0;
int QOI_OP_INDEX = 0x00;
int QOI_OP_DIFF  = 0x40;
int QOI_OP_LUMA  = 0x80;
int QOI_OP_RGB   = 0xfe;
int QOI_OP_RGBA  = 0xff;

int colorsEqual(struct color * c0, struct color * c1)
{
    if(c0->r == c1->r)
    {
        if(c0->g == c1->g)
        {
            if(c0->b == c1->b)
            {
                if(c0->a == c1->a)
                {
                    return 1;
                }
            }   
        }
    }
    return 0;
}
struct color * colorsDiff(struct color * c0,struct color *c1)
{
    struct color * diff = (struct color *)malloc(sizeof(struct color));
    diff->a = c0->a-c1->a;
    diff->b = c0->b  - c1->b;
    diff->g = c0->g - c1->g;
    diff->r = c0->r - c1->r;
    return diff;
}
void main()
{

}