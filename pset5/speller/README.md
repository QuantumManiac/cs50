# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

The word is defined as "a disease of the lungs resulting from the inhalation of very fine silicate or quartz dust." I would also assume that it is one of if not the largest word in the English dictionary.

## According to its man page, what does `getrusage` do?

`getrusage` is used to return resource usage measures.

## Per that same man page, how many members are in a variable of type `struct rusage`?

There are 16 memebers in a variable of type `struct rusage`

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

If we were to pass `before` and `after` by value, instead of reference, then the program would have to copy them into `calculate` which would be inefficient memory and time-wise.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

`main`, once a text file has been loaded, goes through the file character by character to form words. Once it reaches a character that is non-alphanumeric, such as a period or space, and the word it is going through is one letter or more, then it completes said word and references it with the dictionary. Once that is done and mispellings are recorded (or not), the program sets the index to zero, goes to the next word, and the cycle continues. Additionally, if a word is too long or contains a number, then it is ignored.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

I think that `fgetc` was used rather than `fscanf` as by my understanding, it will read the file a character at a time and will be able to skip characters that are not alphanumeric, such as periods and apostrophes.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

The parameters are declared as `const` as they should be constant during the execution of the program and must not be modified.
