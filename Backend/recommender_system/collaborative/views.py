from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, status
import pandas as pd
from collaborative.models import Movie, Rating, Suggestion, userid, Token
from .serializers import RatingSerializer, MovieSerializer, TokenSerializer, RegisterSerializer, useridSerializer
import numpy as np
import tensorflow as tf
from tensorflow import keras
import pandas as pd
from .training_fuctions import cofi_cost_func_v
from django.forms import model_to_dict
from django.db.models import Case, When
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .paginations import CustomNumberPagination, SuggestionsPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
# import requests
# from solana.account import Account
# from solana.rpc.api import Client
# from thor_requests import ThorRequests


# class delete_all(APIView):
#     def get(self, request):
#         Rating.objects.all().delete()
#         return Response('ok')


class Ratings(APIView):
    permission_classes = [IsAuthenticated]

    def get(request):
        name = request.user.username
        idObj = userid.objects.get(username=name)
        idDict = model_to_dict(idObj)
        pk = idDict['userId']
        ratings = Rating.objects.filter(userId=pk)
        ratings_Dict = [model_to_dict(rating) for rating in ratings]
        print(ratings_Dict[0])
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)


class train(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        name = request.user.username
        idObj = userid.objects.get(username=name)
        idDict = model_to_dict(idObj)
        pk = idDict['userId']
        df_R = pd.read_pickle('R.pkl')
        R = df_R.to_numpy()
        df_Y = pd.read_pickle('Y.pkl')
        Y = df_Y.to_numpy()
        df_X = pd.read_pickle('X.pkl')
        X = df_X.to_numpy()
        df_W = pd.read_pickle('W.pkl')
        W = df_W.to_numpy()
        df_b = pd.read_pickle('b.pkl')
        b = df_b.to_numpy()
        num_movies, num_features = X.shape
        num_users, _ = W.shape
        my_ratings = np.zeros(num_movies)
        ratings = Rating.objects.filter(userId=pk)
        ratings_Dict = [model_to_dict(rating) for rating in ratings]
        for i in ratings_Dict:
            ori_id = i['movieId']
            movie_obj = Movie.objects.get(movieId=ori_id)
            serializer_m = MovieSerializer(movie_obj, many=False)
            movie_Dict = model_to_dict(movie_obj)
            movie = int(movie_Dict['id'])
            rating = i['rating']
            my_ratings[movie] = rating
        print('\nNew user ratings:\n')
        for i in range(len(my_ratings)):
            if my_ratings[i] > 0:
                movie_obj = Movie.objects.get(id=i)
                movie_Dict = model_to_dict(movie_obj)
                print(f'Rated {my_ratings[i]} for {movie_Dict["title"]}')
        Y.astype(np.float16)
        R.astype(np.int8)
        Ymean = (np.sum(Y*R, axis=1)/(np.sum(R, axis=1)+1e-12)).reshape(-1, 1)
        Ymean.astype(np.float16)
        Ynorm = Y - np.multiply(Ymean, R)
        Ynorm.astype(np.float16)
        num_movies, num_users = Y.shape
        num_features = 100
        W = tf.Variable(tf.random.normal(
            (num_users,  num_features), dtype=tf.float64),  name='W')
        X = tf.Variable(tf.random.normal(
            (num_movies, num_features), dtype=tf.float64),  name='X')
        b = tf.Variable(tf.random.normal(
            (1,          num_users),   dtype=tf.float64),  name='b')
        optimizer = keras.optimizers.Adam(learning_rate=1e-1)
        iterations = 200
        lambda_ = 1
        for iter in range(iterations):
            with tf.GradientTape() as tape:
                cost_value = cofi_cost_func_v(X, W, b, Ynorm, R, lambda_)
                grads = tape.gradient(cost_value, [X, W, b])
                optimizer.apply_gradients(zip(grads, [X, W, b]))
            if iter % 20 == 0:
                print(f"Training loss at iteration {iter}: {cost_value:0.1f}")
        p = np.matmul(X.numpy(), np.transpose(W.numpy())) + b.numpy()
        pm = p + Ymean
        my_predictions = pm[:, 0]
        movies_to_send = []
        ix = tf.argsort(my_predictions, direction='DESCENDING')
        ix = ix.numpy()
        # ix=ix.to_list()
        print(ix)
        my_rated = [i for i in range(len(my_ratings)) if my_ratings[i] > 0]
        for i in range(41):
            j = ix[i]
            if j not in my_rated:
                print(j)
                movie_obj = Movie.objects.get(id=j)
                movie_Dict = model_to_dict(movie_obj)
                name = movie_Dict['title']
                movies_to_send.append(name)
                print(name)
        for i in range(41):
            j = ix[i]
            if (i == 0):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_1=f'{j}')
            elif (i == 1):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_2=f'{j}')
            elif (i == 2):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_3=f'{j}')
            elif (i == 3):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_4=f'{j}')
            elif (i == 4):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_5=f'{j}')
            elif (i == 5):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_6=f'{j}')
            elif (i == 6):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_7=f'{j}')
            elif (i == 7):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_8=f'{j}')
            elif (i == 8):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_9=f'{j}')
            elif (i == 9):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_10=f'{j}')
            elif (i == 10):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_11=f'{j}')
            elif (i == 11):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_12=f'{j}')
            elif (i == 12):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_13=f'{j}')
            elif (i == 13):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_14=f'{j}')
            elif (i == 14):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_15=f'{j}')
            elif (i == 15):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_16=f'{j}')
            elif (i == 16):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_17=f'{j}')
            elif (i == 17):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_18=f'{j}')
            elif (i == 18):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_19=f'{j}')
            elif (i == 19):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_20=f'{j}')
            elif (i == 20):
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_21=f'{j}')
            # Update suggestion_22 for user with ID pk
            elif i == 22:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_22=f"{j}")
            # Update suggestion_23 for user with ID pk
            elif i == 23:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_23=f"{j}")
            # Update suggestion_24 for user with ID pk
            elif i == 24:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_24=f"{j}")
            # Update suggestion_25 for user with ID pk
            elif i == 25:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_25=f"{j}")
            # Update suggestion_26 for user with ID pk
            elif i == 26:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_26=f"{j}")
            # Update suggestion_27 for user with ID pk
            elif i == 27:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_27=f"{j}")
            # Update suggestion_28 for user with ID pk
            elif i == 28:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_28=f"{j}")
            # Update suggestion_29 for user with ID pk
            elif i == 29:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_29=f"{j}")
            # Update suggestion_30 for user with ID pk
            elif i == 30:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_30=f"{j}")
            # Update suggestion_31 for user with ID pk
            elif i == 31:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_31=f"{j}")
            # Update suggestion_32 for user with ID pk
            elif i == 32:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_32=f"{j}")
            # Update suggestion_33 for user with ID pk
            elif i == 33:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_33=f"{j}")
            # Update suggestion_34 for user with ID pk
            elif i == 34:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_34=f"{j}")
            # Update suggestion_35 for user with ID pk
            elif i == 35:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_35=f"{j}")
            # Update suggestion_36 for user with ID pk
            elif i == 36:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_36=f"{j}")
            # Update suggestion_37 for user with ID pk
            elif i == 37:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_37=f"{j}")
            # Update suggestion_38 for user with ID pk
            elif i == 38:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_38=f"{j}")
            # Update suggestion_39 for user with ID pk
            elif i == 39:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_39=f"{j}")
            # Update suggestion_40 for user with ID pk
            elif i == 40:
                Suggestion.objects.filter(
                    userId=pk).update(suggestion_40=f"{j}")

        return Response('ok')

# @api_view (['GET'])
# def create_suggestions(request):
#     df=pd.read_csv('suggestions.csv',index_col=[0])
#     #print(df)
#     row_iter = df.iterrows()
#     objs = [
#         Suggestion(
#             userId = index,
#             suggestion_1  = row['suggestion_1'],
#             suggestion_2  = row['suggestion_2'],
#             suggestion_3  = row['suggestion_3'],
#             suggestion_4  = row['suggestion_4'],
#             suggestion_5  = row['suggestion_5'],
#             suggestion_6  = row['suggestion_6'],
#             suggestion_7  = row['suggestion_7'],
#             suggestion_8  = row['suggestion_8'],
#             suggestion_9  = row['suggestion_9'],
#             suggestion_10  = row['suggestion_10'],
#             suggestion_11 = row['suggestion_11'],
#             suggestion_12 = row['suggestion_12'],
#             suggestion_13 = row['suggestion_13'],
#             suggestion_14 = row['suggestion_14'],
#             suggestion_15 = row['suggestion_15'],
#             # Extract suggestion_16 from the row and assign it to a variable
#             suggestion_16 = row['suggestion_16'],
#             # Extract suggestion_17 from the row and assign it to a variable
#             suggestion_17 = row['suggestion_17'],
#             # Extract suggestion_18 from the row and assign it to a variable
#             suggestion_18 = row['suggestion_18'],
#             # Extract suggestion_19 from the row and assign it to a variable
#             suggestion_19 = row['suggestion_19'],
#             # Extract suggestion_20 from the row and assign it to a variable
#             suggestion_20 = row['suggestion_20'],
#             # Extract suggestion_21 from the row and assign it to a variable
#             suggestion_21 = row['suggestion_21'],
#             # Extract suggestion_22 from the row and assign it to a variable
#             suggestion_22 = row['suggestion_22'],
#             # Extract suggestion_23 from the row and assign it to a variable
#             suggestion_23 = row['suggestion_23'],
#             # Extract suggestion_24 from the row and assign it to a variable
#             suggestion_24 = row['suggestion_24'],
#             # Extract suggestion_25 from the row and assign it to a variable
#             suggestion_25 = row['suggestion_25'],
#             # Extract suggestion_26 from the row and assign it to a variable
#             suggestion_26 = row['suggestion_26'],
#             # Extract suggestion_27 from the row and assign it to a variable
#             suggestion_27 = row['suggestion_27'],
#             # Extract suggestion_28 from the row and assign it to a variable
#             suggestion_28 = row['suggestion_28'],
#             # Extract suggestion_29 from the row and assign it to a variable
#             suggestion_29 = row['suggestion_29'],
#             # Extract suggestion_30 from the row and assign it to a variable
#             suggestion_30 = row['suggestion_30'],
#             # Extract suggestion_31 from the row and assign it to a variable
#             suggestion_31 = row['suggestion_31'],
#             # Extract suggestion_32 from the row and assign it to a variable
#             suggestion_32 = row['suggestion_32'],
#             # Extract suggestion_33 from the row and assign it to a variable
#             suggestion_33 = row['suggestion_33'],
#             # Extract suggestion_34 from the row and assign it to a variable
#             suggestion_34 = row['suggestion_34'],
#             # Extract suggestion_35 from the row and assign it to a variable
#             suggestion_35 = row['suggestion_35'],
#             # Extract suggestion_36 from the row and assign it to a variable
#             suggestion_36 = row['suggestion_36'],
#             # Extract suggestion_37 from the row and assign it to a variable
#             suggestion_37 = row['suggestion_37'],
#             # Extract suggestion_38 from the row and assign it to a variable
#             suggestion_38 = row['suggestion_38'],
#             # Extract suggestion_39 from the row and assign it to a variable
#             suggestion_39 = row['suggestion_39'],
#             # Extract suggestion_40 from the row and assign it to a variable
#             suggestion_40 = row['suggestion_40']
#         )

#         for index, row in row_iter
#     ]
#     Suggestion.objects.bulk_create(objs)
#     return Response('ok')


class suggestions(ListAPIView, SuggestionsPagination):
    permission_classes = [IsAuthenticated]
    pagination_class = SuggestionsPagination
    serializer_class = MovieSerializer

    def get(self, request):
        name = request.user.username
        idObj = userid.objects.get(username=name)
        idDict = model_to_dict(idObj)
        pk = idDict['userId']
        print(pk)
        suggestions = Suggestion.objects.get(userId=pk)
        suggestions_Dict = model_to_dict(suggestions)
        movieid_to_send = []
        for i in range(15):
            movieid_to_send.append(suggestions_Dict[f'suggestion_{(i+1)}'])
        print(movieid_to_send)
        preserved = Case(*[When(pk=pk, then=pos)
                         for pos, pk in enumerate(movieid_to_send)])
        movie_suggestions = Movie.objects.filter(
            pk__in=movieid_to_send).order_by(preserved)
        page = self.request.query_params.get('page')
        self.queryset = movie_suggestions
        if page is not None:
            paginate_queryset = self.paginate_queryset(movie_suggestions)
            serializer = self.serializer_class(paginate_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(movie_suggestions, many=True)
        return Response(serializer.data)


class genre(ListAPIView, CustomNumberPagination):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomNumberPagination
    serializer_class = MovieSerializer

    def get(self, request, pk):
        if (pk == 'War'):
            movies = Movie.objects.filter(War=1).order_by(
                '-number_of_ratings', '-mean_rating')
        elif (pk == 'Fantasy'):
            movies = Movie.objects.filter(
                Fantasy=1).order_by(-'number_of_ratings', '-mean_rating')
        elif (pk == 'Adventure'):
            movies = Movie.objects.filter(Adventure=1).order_by(
                '-number_of_ratings', '-mean_rating')
        elif (pk == 'Horror'):
            movies = Movie.objects.filter(Horror=1).order_by(
                '-number_of_ratings', '-mean_rating')
        elif (pk == 'Documentary'):
            movies = Movie.objects.filter(Documentary=1).order_by(
                '-number_of_ratings', '-mean_rating')
        elif (pk == 'Mystery'):
            movies = Movie.objects.filter(Mystery=1).order_by(
                '-number_of_ratings', '-mean_rating')
        elif (pk == 'Drama'):
            movies = Movie.objects.filter(Drama=1).order_by(
                '-number_of_ratings', '-mean_rating')
        elif (pk == 'Children'):
            movies = Movie.objects.filter(Children=1).order_by(
                '-number_of_ratings', '-mean_rating')
        elif (pk == 'Romance'):
            movies = Movie.objects.filter(Romance=1).order_by(
                '-number_of_ratings', '-mean_rating')
        elif (pk == 'IMAX'):
            movies = Movie.objects.filter(IMAX=1).order_by(
                '-number_of_ratings', '-mean_rating')
        elif (pk == 'Comedy'):
            movies = Movie.objects.filter(Comedy=1).order_by(
                '-number_of_ratings', '-mean_rating')
        elif (pk == 'Western'):
            movies = Movie.objects.filter(Western=1).order_by(
                '-number_of_ratings', '-mean_rating')
        elif (pk == 'Animation'):
            movies = Movie.objects.filter(Animation=1).order_by(
                '-number_of_ratings', '-mean_rating')
        elif (pk == 'Crime'):
            movies = Movie.objects.filter(Crime=1).order_by(
                '-number_of_ratings', '-mean_rating')
        elif (pk == 'Musical'):
            movies = Movie.objects.filter(Musical=1).order_by(
                '-number_of_ratings', '-mean_rating')
        elif (pk == 'Thriller'):
            movies = Movie.objects.filter(Thriller=1).order_by(
                '-number_of_ratings', '-mean_rating')
        elif (pk == 'Sci_Fi'):
            movies = Movie.objects.filter(Sci_Fi=1).order_by(
                '-number_of_ratings', '-mean_rating')
        elif (pk == 'Action'):
            movies = Movie.objects.filter(Action=1).order_by(
                '-number_of_ratings', '-mean_rating')
        elif (pk == 'Film_Noir'):
            movies = Movie.objects.filter(Film_Noir=1).order_by(
                '-number_of_ratings', '-mean_rating')
        page = self.request.query_params.get('page')
        self.queryset = movies
        if page is not None:
            paginate_queryset = self.paginate_queryset(movies)
            serializer = self.serializer_class(paginate_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(movies, many=True)
        return Response(serializer.data)

# @api_view (['GET'])
# def insert(request):
#     df=pd.read_csv('final_ratings.csv',index_col=[0])
#     #print(df)
#     row_iter = df.iterrows()
#     objs = [
#         Rating(
#             userId  = row['userId'],
#             movieId  = row['movieId'],
#             rating  = row['rating'],
#         )

#         for index, row in row_iter
#     ]
#     Rating.objects.bulk_create(objs)
#     return Response('ok')


@api_view(['GET'])
def create_userid(request, pk):
    id = userid.objects.get_or_create(
        username=pk,
        userId=7001+userid.objects.all().count()
    )
    return Response('ok')


# class RatingCreateView(generics.CreateAPIView):
#     permission_classes=[IsAuthenticated]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class RatingCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class TokenIncrement(APIView):
    permission_classes = [IsAuthenticated]
    serialzer_class = TokenSerializer

    def get(self, request):
        name = request.user.username
        print(name)
        idObj = userid.objects.get(username=name)
        idDict = model_to_dict(idObj)
        print(idDict)
        pk = idDict['userId']
        print(id)
        tokens = Token.objects.get(userId=int(pk))
        token_dict = model_to_dict(tokens)
        new_balance = token_dict['balance']
        new_balance += 10
        Token.objects.filter(userId=int(pk)).update(balance=new_balance)
        tokens = Token.objects.get(userId=int(pk))
        serializer = self.serialzer_class(tokens, many=False)
        return Response(serializer.data)


class RedeemTokens(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        name = request.user.username
        print(name)
        idObj = userid.objects.get(username=name)
        idDict = model_to_dict(idObj)
        print(idDict)
        pk = idDict['userId']
        Token.objects.filter(userId=int(pk)).update(balance=0)
        return Response('ok')


class GetBalance(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TokenSerializer

    def get(self, request):
        name = request.user.username
        print(name)
        idObj = userid.objects.get(username=name)
        idDict = model_to_dict(idObj)
        print(idDict)
        pk = idDict['userId']
        tokens = Token.objects.get(userId=int(pk))
        serializer = self.serializer_class(tokens, many=False)
        return Response(serializer.data)


class update_number(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        print(int(pk))
        movie = Movie.objects.get(movieId=int(pk))
        movie_dict = model_to_dict(movie)
        ratings = movie_dict['number_of_ratings']
        mean = movie_dict['mean_rating']
        rating = int(self.request.query_params.get('rating'))
        print(mean)
        print(ratings)
        new_mean = (mean*ratings+rating)/(ratings+1)
        ratings += 1
        Movie.objects.filter(movieId=int(pk)).update(number_of_ratings=ratings)
        Movie.objects.filter(movieId=int(pk)).update(mean_rating=new_mean)
        return Response('ok')


class Userid(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        name = request.user.username
        idObj = userid.objects.get(username=name)
        idDict = model_to_dict(idObj)
        id = idDict['id']
        print(id)
        print(type(id))
        return Response('OK')


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# class LogoutAllView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request):
#         tokens = OutstandingToken.objects.filter(user_id=request.user.id)
#         for token in tokens:
#             t, _ = BlacklistedToken.objects.get_or_create(token=token)

#         return Response(status=status.HTTP_205_RESET_CONTENT)


class Trending(ListAPIView, CustomNumberPagination):
    pagination_class = CustomNumberPagination
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        movies = Movie.objects.all().order_by('-number_of_ratings')
        serializer = MovieSerializer(movies, many=True)
        page = self.request.query_params.get('page')
        self.queryset = movies
        if page is not None:
            paginate_queryset = self.paginate_queryset(movies)
            serializer = self.serializer_class(paginate_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(movies, many=True)
        return Response(serializer.data)


class Highly_rated(ListAPIView, CustomNumberPagination):
    pagination_class = CustomNumberPagination
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        movies = Movie.objects.all().order_by('-mean_rating')
        serializer = MovieSerializer(movies, many=True)
        page = self.request.query_params.get('page')
        self.queryset = movies
        if page is not None:
            paginate_queryset = self.paginate_queryset(movies)
            serializer = self.serializer_class(paginate_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(movies, many=True)
        return Response(serializer.data)


class GetName(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RegisterSerializer

    def get(self, request):
        user_profile = request.user
        serializer = RegisterSerializer(user_profile)
        return Response(serializer.data)

# class Swap(APIView):
#     permission_classes=[IsAuthenticated]
#     serializer_class=KeysSerializer
#     def get(self, request, pk):
#         keysObj=Key.objects.get(userId=int(pk))
#         keysDict=model_to_dict(keysObj)
#         private_key = keysDict['private_key']
#         destination_address = keysDict['private_key']
#         print(private_key)
#         print(destination_address)
#         # private_key = "<your-private-key>"
#         account = Account.from_secret_key(private_key)
#         solana_client = Client("https://api.mainnet-beta.solana.com")
#         # Connect to the Thorchain API
#         thor = ThorRequests("https://testnet.thornode.thorchain.info/v2")
#         # Fetch the details of the destination chain
#         destination_chain = "ETH"
#         destination_asset = "0xBTC"
#         destination_pool_address = thor.get_destination_pool(destination_chain, destination_asset)
#         # Calculate the expected output amount of the swap
#         input_amount = 1 # in SOL
#         output_amount = thor.get_swap_output(destination_chain, "SOL", destination_asset, input_amount)
#         # Generate a new destination address on the destination chain
#         # destination_address = "<your-destination-address>"
#         # Initiate a swap request with the Thorchain API
#         swap_request = {
#             "source": "SOL",
#             "destination": destination_chain,
#             "asset_from": "SOL",
#             "asset_to": destination_asset,
#             "amount_from": input_amount,
#             "amount_to": output_amount,
#             "memo": "",
#             "recipient": destination_address,
#             "slip": 1,
#             "gas": 0,
#             "gas_rate": 0,
#             "mode": "fast",
#         }
#         signed_request = thor.sign_swap_request(swap_request, private_key)
#         response = thor.submit_swap_request(signed_request)
#         # Submit the transaction to the Solana network
#         transaction = solana_client.send_transaction(signed_request["transaction"], account)
#         # Wait for the transaction to be confirmed
#         confirmed = solana_client.get_confirmed_transaction(transaction["result"])
#         # Monitor the Thorchain transaction pool for the swap to be processed
#         swap_hash = response["swap_id"]
#         swap_status = thor.get_swap_status(swap_hash)
#         while swap_status != "success":
#             swap_status = thor.get_swap_status(swap_hash)
#         return Response('ok')


@api_view(['GET'])
def delete_all(request):
    Movie.objects.all().delete()
    return Response('ok')


@api_view(['GET'])
def insert(request):
    df = pd.read_csv('movies_with_details.csv', index_col=[0])
    # print(df)
    row_iter = df.iterrows()
    objs = [
        Movie(
            id=index,
            mean_rating=row['mean_rating'],
            number_of_ratings=row['number_of_ratings'],
            title=row['title'],
            War=row['War'],
            Fantasy=row['Fantasy'],
            Adventure=row['Adventure'],
            Horror=row['Horror'],
            Documentary=row['Documentary'],
            Mystery=row['Mystery'],
            Drama=row['Drama'],
            Children=row['Children'],
            Romance=row['Romance'],
            IMAX=row['IMAX'],
            Comedy=row['Comedy'],
            Western=row['Western'],
            Animation=row['Animation'],
            No_genre=row['No_genre'],
            Crime=row['Crime'],
            Musical=row['Musical'],
            Thriller=row['Thriller'],
            Action=row['Action'],
            Sci_Fi=row['Sci_Fi'],
            Film_Noir=row['Film_Noir'],
            movieId=row['movieId'],
            backdrop_path=row['backdrop_path'],
            poster_path=row['poster_path'],
            tmdb_title=row['tmdb_title'],
            tagline=row['tagline'],
            overview=row['overview'],
            budget=row['budget'],
            runtime=row['runtime'],
            original_language=row['original_language'],
        )

        for index, row in row_iter
    ]
    Movie.objects.bulk_create(objs)
    return Response('ok')
