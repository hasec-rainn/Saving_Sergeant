# Scanner Implementation
The implementation of the scanner will involve understanding the scanner well enough to have it take receipts and store them as csv's in the proper [[Data Format]]

### Improving OCR Accuracy

- [x] Grayscale
- [x] Binarization
- [x] Correct page segmentation (psm)
- [ ] Resizing
	- [x] 50% Scale
	- [x] Dynamic resizing via bounding box measurements
- [x] Custom training data (`tessdata_best`)
- [x] Whitelisting characters
- [x] Image segmentation (no improvement)
- [ ] See if "right-hand text bug" can be replicated on other

### References
https://groups.google.com/g/tesseract-ocr/c/Wdh_JJwnw94/m/24JHDYQbBQAJ
https://stackoverflow.com/questions/64547823/does-tesseract-do-image-resizing-internally
https://stackoverflow.com/questions/31633403/tesseract-receipt-scanning-advice-needed
https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html
