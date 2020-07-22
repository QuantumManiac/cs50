# Questions

## What's `stdint.h`?

'stdint.h' is a header file in C that when used defines integer types with specified widths.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

The point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program is to restrict an integer to an exact width. For example, `uint8_t` is restricted to eight bits.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

A `BYTE` is 1 byte, a `DWORD` is 4 bytes, a `LONG` is 4 bytes, and a `WORD` is 2 bytes

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

The first two bytes of any BMP file, which is a `WORD` named `bfType`,  must be `BM`. This identifies the filetype.

## What's the difference between `bfSize` and `biSize`?

The difference between `bfSize` and `biSize` is that while `bfSize` specifies the size of the bitmap file in bytes, `biSize` specifies the size of the structure in bytes.

## What does it mean if `biHeight` is negative?

If `biHeight` is negative, the bitmap is a top-down DIB (Device Independent Bitmap) and its origin is the top-left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

The field `biBitCount` specifies the BMP's color depth or bits per pixel.

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

`fopen` may return `NULL` in lines 24 and 32 if a file cannot be found or cannot be written to.

## Why is the third argument to `fread` always `1` in our code?

The third argument to `fread` is always `1` because the program reads one element at a time.

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

Line 65 of `copy.c` assigns 3 to `padding` if `bi.biWidth`.

## What does `fseek` do?

`fseek` can be used to skip over any padding in the BMP and go to the next RGBTriple.

## What is `SEEK_CUR`?

`SEEK_CUR` provides the current position in the file that the program is on.

## Whodunit?

`It was Professor Plum with the candlestick in the library`
