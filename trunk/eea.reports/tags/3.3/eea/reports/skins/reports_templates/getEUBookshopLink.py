##parameters=order_id=None,REQUEST=None
if not order_id:
    return 'http://bookshop.europa.eu/is-bin/INTERSHOP.enfinity/WFS/EU-Bookshop-Site/en_GB/-/EUR/ViewStandardCatalog-Browse?CatalogCategoryID=mysKABstXFIAAAEjDIcY4e5K'
return 'http://bookshop.europa.eu/is-bin/INTERSHOP.enfinity/WFS/EU-Bookshop-Site/en_GB/-/EUR/ViewParametricSearch-SimpleOfferSearch?webform-id=WFSimpleSearch&DefaultButton=findSimple&WFSimpleSearch_NameOrID=%(order)s&SearchConditions=&SearchType=1' % {
    'order': order_id
}
