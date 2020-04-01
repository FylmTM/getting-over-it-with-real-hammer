package gettingoverit

import org.opencv.core.Core
import org.opencv.core.CvType
import org.opencv.core.Mat
import org.opencv.core.Scalar

fun main() {
    System.loadLibrary(Core.NATIVE_LIBRARY_NAME)

    println("hello")
    println("Welcome to OpenCV " + Core.VERSION)
    val m = Mat(5, 10, CvType.CV_8UC1, Scalar(0.0))
    println("OpenCV Mat: $m")
    val mr1: Mat = m.row(1)
    mr1.setTo(Scalar(1.0))
    val mc5: Mat = m.col(5)
    mc5.setTo(Scalar(5.0))
    println(
        """
            OpenCV Mat data:
            ${m.dump()}
            """.trimIndent()
    )
}
