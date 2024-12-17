from PIL import Image
import io

class ImageProcessor:
    def __init__(self):
        self.supported_formats = {'image/jpeg', 'image/png'}
    
    async def process(self, file):
        """
        处理上传的图片文件
        """
        if file.content_type not in self.supported_formats:
            raise ValueError("Unsupported image format")
        
        content = await file.read()
        image = Image.open(io.BytesIO(content))
        
        # 在这里添加图像预处理步骤
        # 1. 调整大小
        # 2. 优化质量
        # 3. 标准化
        
        return image 