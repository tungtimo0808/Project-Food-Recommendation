import pandas as pd

# Đọc dữ liệu từ file CSV
data = pd.read_csv(r'C:\Users\ngthd\Downloads\FINAL_ML2_Recipe\FINAL_ML2_Recipe\covereal.csv')

# Kiểm tra các tên cột trong dataset
print(data.columns)

# Tạo cột 'Low_Carb' cho chế độ ăn Low-Carb (Keto, Paleo)
# Các món ăn Low-Carb cần ít carbs (dưới 20g mỗi khẩu phần) và có lượng chất béo cao
data['Low_Carb'] = ((data['Carbs'] <= 20) & (data['Fat'] > 10)).astype(int)

vegetarian_ingredients = [
    'acorn squash', 'aioli', 'ajo', 'ajwain', 'alcohol', 'ale', 'allspice', 'almonds', 'amaretti biscuits', 
    'amaretto', 'angelica', 'anise', 'aniseed', 'aperol', 'apple', 'apricot', 'armagnac', 'arrabbiata sauce', 
    'artichoke', 'asafoetida', 'asparagus', 'aubergine', 'avocado','blueberries', 'bloomer', 'blancmange', 'blackberries', 'black peppercorns', 'black olives', 'bitters',
    'biscuits', 'biscotti', 'baps', 'barolo', 'basil', 'basmati rice', 'bay leaves', 'biber', 'berries',
    'berkswell', 'beets', 'bean', 'beansprouts', 'beetroot', 'broad beans', 'briks', 'brie', 'breadcrumbs', 'bread flour', 'bread', 'bran', 'brambles', 'bourguignon',
    'borlotti beans', 'bok choi', 'banana', 'baby capers', 'baby leeks', 'baguette', 'bagel','cashew nuts', 'carrot', 'cardamom pods', 'cardamom', 'caramel', 'capsicum', 'capers', 'caperberries', 
    'cannelloni tubes', 'camembert', 'cake', 'cabbage', 'butternut squash', 'butternut', 'buttercream', 
    'burrata', 'bun', 'bucatini', 'brown sugar', 'broccoli','cashews', 'chilli', 'chicory', 'chickpeas', 'chickpea flour', 'chestnuts', 'chervil', 'cherry tomatoes',
    'cherry', 'cherries', 'cheese', 'cheddar', 'caster sugar', 'cauliflower', 'celeriac', 'celery', 'chapatis','chilli oil', 'chipotle paste', 'chips', 'chives', 'chocolate', 'choi', 'choi sum', 'choy', 'ciabatta', 
    'cider', 'cinnamon', 'cinnamon stick', 'clementine', 'clementine juice', 'clove', 'cobbettes', 'cocoa', 
    'cocoa powder', 'coconut',
    'chanterelles','coconut flakes', 'coconut milk', 'coconut oil', 'coffee', 'coleslaw', 'compote', 'cordial', 'coriander',
    'coriander seeds', 'corn', 'corn cobs', 'cornbread', 'cornflakes', 'cornflour', 'cornichons', 'cornmeal',
    'cottage cheese', 'courgette', 'courgette flowers', 'couscous', 'crackers', 'crackling', 'cranberries',
    'cream', 'crema', 'cress', 'crisps', 'crostini', 'crumpet', 'cucumber', 'cumin', 'cumin seeds', 'cupcakes',
    'currants', 'curry leaves', 'custard','elderflower cordial', 'emmental', 'endive', 'epazote', 'espresso', 'farfalle', 'fennel', 'fennel seeds', 
    'fenugreek', 'fenugreek leaves', 'fenugreek seeds', 'feta', 'feta cheese', 'fig', 'flatbread', 'flaxseed', 
    'flour', 'flowering oregano', 'fraiche', 'frangipane', 'fresh fruit', 'frozen', 'frozen peas', 'fruit', 
    'fudge', 'furikake', 'fusilli', 'galangal', 'garam masala', 'garlic', 'gelatine', 'gem', 'gemelli', 'ghee', 'gherkin', 'ginger', 
    'gingernut biscuits', 'glaze', 'glucose', 'gnocchi', 'gochujang', 'golden syrup', 'gooseberries', 'gordal',
    'gorditas', 'grain', 'granary bread', 'granola', 'granules', 'grapefruit', 'grapes', 'gravy', 'green beans', 
    'greens',    'ground cumin', 'groundnut oil', 'guacamole', 'gum', 'halloumi', 'hanout', 'harissa', 'hazelnuts', 'herbs',
    'hobnobs', 'hollandaise', 'honey', 'honeycomb', 'horlicks', 'horseradish', 'houmous', 'icing sugar', 'ipa',
    'jam', 'jelly', 'juniper berries', 'kabocha', 'kale', 'kernels', 'ketchup',  'kimchee', 'kimchi', 'kirsch', 'kiwi', 'knuckle', 'labneh', 'lager', 'leche', 'leek', 'lemon', 'lemon zest',
    'lemonade', 'lemongrass', 'lentil', 'lettuce', 'lime', 'lime juice', 'lime leaves', 'limoncello', 'linguine', 
    'linseed', 'loaf', 'macaroni', 'mace', 'madeira', 'madeira sponge', 'malbec', 'maltesers', 'manchego', 'mandarin',
    'mangetout', 'mango', 'mango chutney', 'margarine', 'maria', 'marinated olives', 'marjoram', 'marmalade',
    'marnier', 'marsala', 'marshmallows', 'marzipan', 'masala', 'mascarpone', 'matchsticks', 'mayonnaise', 'melon', 'meringue', 'methi', 'milk', 'mince', 'minced', 'mini tortillas', 'mint', 'mirin', 
    'mixed spice', 'mooli', 'mozarella', 'mozzarella', 'muffins', 'mushroom', 'mussel', 'mustard', 'mustard seeds',
    'natural yogurt', 'nectar', 'nectarine','negra', 'nettles', 'noir', 'noodles', 'nori', 'nutella', 'nutmeg', 'nuts', 'oatmeal', 'oats', 'oelek', 'oil',
    'okra', 'olive oil', 'olives', 'onion', 'orange', 'orange juice', 'orange zest', 'orecchiette', 'oregano',
    'orzo', 'ovaltine', 'padano', 'palm sugar', 'pancakes', 'paneer',  'paneer cheese', 'panettone', 'pangrattato', 'pappardelle', 'paprika', 'parathas', 'parma', 'parmesan', 
    'parsley', 'parsnip', 'passata', 'passion fruit', 'pasta', 'pastina', 'pastry', 'pea shoots', 'peach', 
    'peanuts', 'pear', 'pearl barley', 'peas', 'pecans', 'pecorino', 'pecorino cheese', 'pectin', 'peel', 
    'penne', 'pepper',    'peppercorn', 'peppermint', 'pesto', 'piccalilli', 'pickle', 'pie', 'pimms', 'pineapple', 'pinenuts', 'pisco',
    'pistachios', 'pistou', 'pittas', 'plain flour', 'plantain', 'plum', 'plum tomatoes', 'polenta', 'pollen',
    'pomegranate', 'pomegranate juice', 'popcorn', 'poppadoms', 'poppy', 'porcini',    'port', 'porter', 'potato', 'prosecco', 'provence', 'prune', 'puff pastry', 'pulp', 'pumpkin', 'pumpkin seeds',
    'quince', 'quinoa', 'radicchio', 'radish', 'raisins', 'raita', 'rapeseed oil', 'raspberries', 'recado', 
    'red pepper', 'redcurrant', 'relish',  'rhubarb', 'rice', 'rice vinegar', 'ricotta', 'ricotta cheese', 'riesling', 'rigatoni', 'rind', 'roasted peppers',
    'rocket', 'rose petals', 'rosemary', 'rosewater', 'rossa', 'royals', 'saffron', 'sage', 'sage leaves', 'sake',
    'salata', 'salsa', 'salt', 'samphire','satsuma', 'sauerkraut', 'savory', 'scamorza', 'scones', 'sea salt', 'seaweed', 'sec', 'semolina', 'sesame',
    'sesame oil', 'sesame seeds', 'shallot', 'sherry', 'sherry vinegar', 'short pasta', 'shortbread', 'shortening',
    'shredded suet', 'silken tofu', 'slaw', 'smarties', 'wholemeal', 'williams', 'wine', 'wine vinegar', 'yams', 'yeast', 'yoghurt', 'yogurt', 'yuzu', 'zucchini','turmeric', 'turnip', 'tzatziki', 'unsalted peanuts', 'vanilla essence', 'vanilla extract', 'vanilla pod', 
    'vegemite', 'vegetable oil', 'verde', 'vermicelli', 'vermouth', 'vinegar', 'vodka', 'walnuts', 'wasabi', 
    'water', 'water chestnuts', 'watercress', 'watermelon', 'weetabix', 'wheat', 'whiskey', 'whisky', 'white cabbage',
    'white wine', 'whole milk','sweetcorn', 'sweets', 'syrup', 'tabasco', 'tablet', 'tacos', 'tagliatelle', 'taglierini', 'tagliolini', 
    'tahini', 'tamari', 'tamarind', 'tangerine', 'tapenade', 'tarragon', 'tartare sauce', 'tea', 'templegall', 
    'thyme', 'tikka', 'toffees', 'tofu', 'tomato', 'tortellini', 'tortilla', 'treacle','sofrito', 'soup', 'sourdough', 'soy sauce', 'spaghetti', 'spinach', 'sponge', 'spring onions', 
    'sprouting broccoli', 'sprouts', 'squash', 'sriracha', 'star anise', 'stone fruit', 'stout', 'strawberries',
    'strawberry', 'suet', 'sugar', 'sultanas', 'sumac', 'swede', 'sweet potato', 'sweet sherry'
]
# Danh sách nguyên liệu cần loại bỏ cho món ăn chay
non_vegetarian_ingredients = [
    'anchovies', 'anchovy fillets', 'andouille','beef', 'beef mince', 'belly','brisket', 'bresaola', 'bream', 'brandy', 'bourbon',
    'bologna', 'bolognese', 'bacon', 'baileys','campari', 'calvados', 'buttermilk', 'butter', 'butterghee', 'chicken stock', 
    'chicken breasts', 'chicken', 'chianti', 'chardonnay', 'champagne', 'chipolata', 'chops', 'chorizo', 'clam', 'cockles',
    'cognac', 'cointreau', 'crabmeat', 'cumberlands',
    'drambuie', 'drumsticks', 'duck', 'duck breast', 'duck leg','dal', 'dare', 'dark chocolate', 'dashi', 'date', 'demerara sugar', 'deseeded', 'desiccated coconut', 
    'dill', 'dressing', 'dried apricots', 'dried fruit', 'dripping', 'dukkah', 'dumplings','egg', 'egg yolks', 'escallopes', 'fish sauce',
    'galliano', 'gin', 'grappa','grouse', 'guinness', 'haggis', 'ham', 'hogget', 'kidneys', 'king prawns', 'lamb', 
    'lamb cutlets', 'lamb mince', 'lamb neck', 'lamb shoulder', 'lard', 'lardons', 'liqueur', 'liquor', 'liver', 'lobster', 'mackerel', 'marrow',
    'meat stock', 'meatballs', 'minced lamb', 'mincemeat', 'monkfish fillets', 'mortadella', 'mutton', 'nduja', 'partridge', 'pastrami',
    'pheasant', 'pigeons', 'pork', 'pork loin', 'porchetta',   'pork mince', 'pork ribs', 'pork shoulder', 'poussins', 'prawn', 'prosciutto', 'rabbit', 'quail',
    'oyster', 'oyster sauce', 'pancetta',    'roe', 'salami', 'salmon', 'sardines', 'rum', 'rump',
    'sausage', 'sausagemeat', 'scallop', 'shanks', 'shrimp', 'sirloin', 'skirt',
    'veal', 'venison', 'white fish','tenderloin', 'tequila', 'tuna', 'turkey','smoked trout', 'speck', 'squid', 'steak', 'stichelton', 'stilton','yolks'
    
    
]
# Tạo cột 'Vegetarian' dựa trên nguyên liệu trong cột 'Ingredients'
data['Vegetarian'] = data['Ingredients'].apply(lambda x: 1 if any(veg in x.lower() for veg in vegetarian_ingredients) and not any(non_veg in x.lower() for non_veg in non_vegetarian_ingredients) else 0)

# Nếu muốn đánh số từ 1 đến N
data['k'] = range(1, len(data)+1)

# Tạo output với các cột 'Dish Name', 'Vegetarian', 'Low_Carb'
output = data[['Dish Name', 'Vegetarian', 'Low_Carb']]  

# Lưu kết quả vào file CSV mới
output.to_csv(r'C:\Users\ngthd\Downloads\FINAL_ML2_Recipe\FINAL_ML2_Recipe\classified_recipes.csv', index=False)

# Hiển thị 5 dòng đầu của dữ liệu đã phân loại
output.head()

# Hiển thị số lượng món ăn theo loại Vegetarian
print("Số lượng món ăn theo loại Vegetarian:")
print(data['Vegetarian'].value_counts())

# Hiển thị số lượng món ăn theo loại Low_Carb
print("Số lượng món ăn theo loại Lowcarbs:")
print(data['Low_Carb'].value_counts())