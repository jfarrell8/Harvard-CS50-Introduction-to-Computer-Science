# Questions

## What's `stdint.h`?

// Header that declares sets of integers of defined widths (# of bits used to store value)

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

// Designates an integer type with an exact bit width

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

// BYTE: 1 bytes; DWORD: 4 bytes; LONG: 4 bytes; WORD: 2 bytes

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

// 42 4d

## What's the difference between `bfSize` and `biSize`?

// bfSize: size in bytes of the bmp file; biSize: size in bytes required by the structure

## What does it mean if `biHeight` is negative?

// bmp file is top-down, and origin is upper-left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

// biBitCount

## Why might `fopen` return `NULL` in `copy.c`?

// file doesn't exist

## Why is the third argument to `fread` always `1` in our code?

// There's only 1 element to be read

## What value does `copy.c` assign to `padding` if `bi.biWidth` is `3`?

// 3

## What does `fseek` do?

// Sets stream indicator to new position

## What is `SEEK_CUR`?

TODO
