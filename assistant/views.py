from django.shortcuts import render,redirect, HttpResponse
from assistant.forms import CustomUserForm
from django.contrib.auth import authenticate,login,logout
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import pywhatkit
# Create your views here.

def register(request):
    form = CustomUserForm()
    if request.method == "Post":
        form = CustomUserForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect("login")
        
    context = {"form":form}
    return render(request, 'register.html',context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
        else:
            return HttpResponse("user is empty")
    
    return render(request,'login.html')



def chatbot_view(request):
    chat_history = []  # Empty list to store chat history

    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        print("user input: ",user_input)
        # Load the pre-trained model and tokenizer
        model = GPT2LMHeadModel.from_pretrained("gpt2")
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

        # Generate response
        inputs = tokenizer.encode(user_input, return_tensors="pt")
        outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Append current user input and generated response to chat history
        chat_history.append((user_input, generated_text))
        if 'paly' in user_input:
            song = user_input.replace('play','')
            # talk('playing' + song)
            pywhatkit.playonyt(song)    
    context = {'chat_history': chat_history}
    return render(request, 'chat.html',context)


