from haystack import indexes
from goods.models import GoodsModel


# 这个文件的作用是设置haystack在生成索引时，根据那些字段来生成索引
class GoodsModelIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return GoodsModel

    def index_queryset(self, using=None):
        return self.get_model().objects.all()