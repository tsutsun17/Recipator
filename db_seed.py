import pandas as pd
from line_app.models import Recipe

if __name__ == '__main__':
    recipes = Recipe.get_all_recipes()
    print('Recipeのデータを更新します: {}'.format(len(recipes)))
    if len(recipes)!=0:
        Recipe.delete_recipes()
    recipes = Recipe.get_all_recipes()
    print("Recipeを全削除しました: {}件".format(len(recipes)))

    df = pd.read_csv('line_app/data/recipe_data_no_dup.csv')
    recipe_n = len(df)
    for i in range(recipe_n):
        recipe_index = i
        name = df['料理名'][i]
        image_url = df['画像'][i]
        recipe_url = df['URL'][i]
        recipe = Recipe(recipe_index, name, image_url, recipe_url)
        recipe.commit_db()

    recipes = Recipe.get_all_recipes()
    print('Recipeを全部登録しました: {}件'.format(len(recipes)))

