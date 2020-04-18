import React from 'react';
import PDFViewer from 'pdf-viewer-reactjs';
import file from '../assets/samples.pdf';
 
const ReportRenderer = () => {
    return (
        <PDFViewer
            document={{
                url: file,
            }}
        />
    )
}
 
export default ReportRenderer