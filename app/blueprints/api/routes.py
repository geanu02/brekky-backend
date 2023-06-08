from flask import request, jsonify
from . import bp
from app import db
from app.models import User, UserRecipe, UserSchema, UserRecipeSchema
from app.blueprints.api.helpers import token_required

# Instantiate Schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_recipe_schema = UserRecipeSchema()
user_recipes_schema = UserRecipeSchema(many=True)

# Add UserRecipe
@bp.route('/add', methods=["POST"])
@token_required
def add_recipe(user):
    content = request.json
    userById = User.query.filter_by(user_id=user.user_id).first()
    if userById:
        rec = UserRecipe(
            user_id = user.user_id,
            recipe_id = content['recipe_id'],
            recipe_title = content['recipe_title'],
            recipe_thumb = content['recipe_thumb'],
            recipe_api_content = content['recipe_api_content'],
            recipe_user_content = content['recipe_user_content'],
            recipe_api_url = content['recipe_api_url']
        )
        rec.commit()
        return jsonify({
            "message": f"User Recipe {rec.user_recipe_id} successfully added!",
            "userRecipeId": rec.user_recipe_id,
            "userRecipeTitle": rec.recipe_title,
            "recipeId": rec.recipe_id,
            "success": True
        })
    else:
        return jsonify({
        "message": "Post unsuccessful.",
        "success": False
    })

# Get User Recipe by User Recipe ID 
@bp.route('/get/<user_recipe_id>', methods=["GET"])
# @token_required
# def get_recipe(user, user_recipe_id):
def get_recipe(user_recipe_id):
    recipe = UserRecipe.query.filter_by(user_recipe_id=user_recipe_id).first()
    if recipe:
        result = user_recipe_schema.dump(recipe)
        return jsonify(result)
    return jsonify({
        "message": f"User Recipe ID: {user_recipe_id} does not exist.",
        "success": False
    })

# Get All User Recipes by User ID
@bp.route('/getall/<username>', methods=["GET"])
# @token_required
#def get_all_user_recipes(user, username):
def get_all_user_recipes(username):
    chosenUser = User.query.filter_by(username=username).first()
    if chosenUser:
        result = user_recipes_schema.dump(chosenUser.user_recipe)
        result.update({
            "message": f"{username} has recipes.",
            "success": True
        })
        return jsonify(result)
    return jsonify({
        "message": f"{username} does not have recipes.",
        "success": False
    })

# Update User Recipe by User Recipe ID
@bp.route('/recipe/<user_recipe_id>', methods=["POST", "PUT"])
@token_required
def update_recipe(user, user_recipe_id):
    recipe = UserRecipe.query.filter_by(user_recipe_id=user_recipe_id).first()
    if recipe:
        recipe.recipe_user_content = request.json
        recipe.commit()
        result = user_recipe_schema.dump(recipe)
        result.update({"message": f"User Recipe ID: {user_recipe_id} has been updated successfully."})
        return jsonify(result)
    return jsonify({
        "message": f"User Recipe ID: {user_recipe_id} does not exist.",
        "success": False
    })

# Delete User Recipe by User Recipe ID
@bp.route('/recipe/<user_recipe_id>', methods=["DELETE"])
@token_required
def delete_recipe(user, user_recipe_id):
    recipe = UserRecipe.query.filter_by(user_recipe_id=user_recipe_id).first()
    if recipe:
        db.session.delete(recipe)
        recipe.commit()
        return jsonify({
            "message": f"User Recipe ID: {user_recipe_id} has been deleted.",
            "success": True
        })
    return jsonify({
        "message": f"User Recipe ID: {user_recipe_id} does not exist.",
        "success": False
    })