import axios from 'axios'; //make async requests
import { GET_CATEGORY } from './types';

//get category
export const getCategory = () => dispatch => {
	//make get request
	axios
		.get('exchange/api/category')
		.then(res => {
			dispatch({
				type: GET_CATEGORY,
				payload: res.data
			});
		})
		.catch(err => console.log(err));
}