This is the implementation for a web application on local server, though it is working
very slow compared to the actual program.

Reason for being slow is that we're using the library instead of a pre-trained model
that calls each frame and implements a face recognition algorithm from scratch every time.