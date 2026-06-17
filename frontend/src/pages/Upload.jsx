import PageHeader from '../components/ui/PageHeader.jsx';
import UploadPanel from '../components/upload/UploadPanel.jsx';

export default function Upload() {
  return (
    <>
      <PageHeader
        eyebrow="Image Intake"
        title="Upload Traffic Evidence"
        description="Submit traffic camera images for violation detection, OCR extraction, and evidence record creation."
      />
      <UploadPanel />
    </>
  );
}

