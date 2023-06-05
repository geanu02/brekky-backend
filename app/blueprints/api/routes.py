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
@bp.post('/add', methods=["POST"])
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

