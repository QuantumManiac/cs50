// Helper functions for music

#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    int num = fraction[0] - 48;
    int den = fraction[2] - 48;
    return (num * (8 / den));
}

// Calculates frequency (in Hz) of a note
// A4 is 440Hz
// Finding frequency: 2^n/12 * 440 where n is semitones right from A440 (neg if left)
// Example of Input: D#3
int frequency(string note)
{
    double semitone = 0;
    char scale = note[0];
    int octave = -48;
    // For notes with accidentals
    if (strlen(note) == 3)
    {
        char accidental = note[1];
        octave += note[2];
        if (scale == 'B')
        {
            semitone += 2;
        }
        else if (scale >= 'F' && scale <= 'G')
        {
            semitone += (scale - 'H') * 2;
        }
        else if (scale <= 'E' && scale >= 'C')
        {
            semitone += (scale - 'H') * 2 + 1;
        }
        semitone += (octave - 4) * 12;
        if (accidental == 'b')
        {
            semitone--;
        }
        else
        {
            semitone++;
        }
    }
    // For notes without accidentals
    else
    {
        octave += note[1];
        if (scale == 'B')
        {
            semitone += 2;
        }
        else if (scale >= 'F' && scale <= 'G')
        {
            semitone += (scale - 'H') * 2;
        }
        else if (scale <= 'E' && scale >= 'C')
        {
            semitone += (scale - 'H') * 2 + 1;
        }
        semitone += (octave - 4) * 12;
    }
    int frequency = (round((440 * (pow(2, semitone / 12)))));
    return frequency;
}


// Determines whether a string represents a rest
bool is_rest(string s)
{
    if (s[0] == '\0')
    {
        return true;
    }
    else
    {
        return false;
    }
}