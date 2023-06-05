from flask import request, jsonify
import json
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
            "message": f"Recipe {rec.recipe_id} successfully posted!",
            "success": True
        })
    else:
        return jsonify({
        "message": "Post unsuccessful.",
        "success": False
    })

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
