import pickle
import streamlit as st
import pandas as pd
import numpy as np
 
# loading the trained model
pickle_in = open('classifier.pkl', 'rb') 
classifier = pickle.load(pickle_in)
 
@st.cache()

def csv_to_df():
    st.set_option('deprecation.showfileUploaderEncoding', False)#to remove error
    st.subheader("Please Upload Your Dataset")
    data=st.file_uploader("Upload your dataset",type=['csv'])
    if data is not None:
        df = pd.read_csv(data)
        st.dataframe(df.head(10))
        st.success("Data Successfully loaded")
        model = pickle.load(open("classifier.pkl", "rb"))


# defining the function which will make the prediction using the data which the user inputs 
def prediction(step, transaction_type, amount, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, isFlaggedFraud):   
 
    # Pre-processing user input    
    if transaction_type == "CASH-IN":
        transaction_type = 0
    elif transaction_type == "CASH-OUT":
        transaction_type = 1
    elif transaction_type == "DEBIT":
        transaction_type = 2
    elif transaction_type == "PAYMENT":
        transaction_type = 3
    else:
        transaction_type = 4
 
    if isFlaggedFraud == "0":
        isFlaggedFraud = 0
    else:
        isFlaggedFraud = 1  
 
 
    # Making predictions 
    prediction = classifier.predict( 
        np.array([step, transaction_type, amount, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, isFlaggedFraud]).reshape(1, -1)
        )
     
    if prediction == 0:
        pred = 'Fraud transaction'
    else:
        pred = 'Safe transaction'
    return pred
      
  
# this is the main function in which we define our webpage  
def main():       
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:yellow;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Fraud Transactions In Shell Companies</h1> 
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
      
    # following lines create boxes in which user can enter data required to make prediction 
    # step = st.number_input("Step") 
    # transaction_type = st.selectbox('Tansaction Type',("CASH-IN","CASH-OUT", "DEBIT", "PAYMENT", "TRANSFER"))
    # amount = st.number_input("Amount paid") 
    # oldbalanceOrg = st.number_input("Old Balance")
    # newbalanceOrig	 = st.number_input("New Balance")
    # nameDest = st.number_input("Destination Account")
    # oldbalanceDest = st.number_input("Old Balance Destination")
    # isFlaggedFraud = st.selectbox('Fraud',("0","1"))
    result =""
    st.set_option('deprecation.showfileUploaderEncoding', False)#to remove error
    st.set_option('deprecation.showfileUploaderEncoding', False)#to remove error
    st.subheader("Please Upload Your Dataset")
    data=st.file_uploader("Upload your dataset",type=['csv'])
    if data is not None:
        df = pd.read_csv(data)
        st.dataframe(df.head(10))
        st.success("Data Successfully loaded")
        model = pickle.load(open("classifier.pkl", "rb"))

        def preprocessData(dataFrame):
                #dataFrame = dataFrame.drop('step','nameOrig','nameDest'],axis = 1)
                dataFrame = dataFrame.drop(['Unnamed: 0'],axis=1)

                x_new = dataFrame
                x_new = pd.get_dummies(x_new)
                return x_new
        
        if st.button("Predict"):
                st.balloons()
                x_new = preprocessData(df)
               
                df['y_prednew'] = model.predict(x_new)
                df.to_csv('final_result.csv')

                st.title("Your Output is")
                print("here")
                st.dataframe(df)
    
      
    # when 'Predict' is clicked, make the prediction and store it 
    # if st.button("Predict"): 
    #     result = prediction(step, transaction_type, amount, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, isFlaggedFraud)
    #     st.success('Its a {}'.format(result))
    #     print(transaction_type)
     
if __name__=='__main__': 
    main()