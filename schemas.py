from marshmallow import Schema, fields


class DirectorSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class GenreSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class MovieSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    trailer = fields.String()
    year = fields.Integer()
    rating = fields.Float()
    genre_id = fields.Integer()
    genre = fields.Nested(GenreSchema)
    director_id = fields.Integer()
    director = fields.Pluck(field_name="name", nested=DirectorSchema)
