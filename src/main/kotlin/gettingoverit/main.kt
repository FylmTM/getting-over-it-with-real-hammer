package gettingoverit

import org.opencv.core.Core
import org.opencv.core.MatOfRect
import org.opencv.core.Point
import org.opencv.core.Scalar
import org.opencv.imgcodecs.Imgcodecs
import org.opencv.imgproc.Imgproc
import org.opencv.objdetect.CascadeClassifier

object GettingOverIt {
}

fun main() {
    System.loadLibrary(Core.NATIVE_LIBRARY_NAME)

    // Create a face detector from the cascade file in the resources
    // directory.
    val faceDetector =
        CascadeClassifier("C:\\tool\\opencv\\opencv\\build\\etc\\lbpcascades\\lbpcascade_frontalface.xml")
    val image = Imgcodecs.imread("C:\\work\\getting-over-it\\src\\main\\resources\\lena.png")

    // Detect faces in the image.
    // MatOfRect is a special container class for Rect.

    // Detect faces in the image.
    // MatOfRect is a special container class for Rect.
    val faceDetections = MatOfRect()
    faceDetector.detectMultiScale(image, faceDetections)

    println(String.format("Detected %s faces", faceDetections.toArray().size))

    // Draw a bounding box around each face.
    for (rect in faceDetections.toArray()) {
        Imgproc.rectangle(
            image,
            Point(rect.x.toDouble(), rect.y.toDouble()),
            Point((rect.x + rect.width).toDouble(), (rect.y + rect.height).toDouble()),
            Scalar(0.0, 255.0, 0.0)
        )
    }
    // Save the visualized detection.
    val filename = "faceDetection.png"
    println(String.format("Writing %s", filename))
    Imgcodecs.imwrite(filename, image)
}
