import React, { Component, Fragment } from 'react';
import ReactDOM from 'react-dom';

import Header from './layout/header';
import Searchbar from './layout/Searchbar';

import { Provider } from 'react-redux';
import store from '../store';

class App extends Component {
	render() {
		return (
			<Provider store={store}>
				<Fragment>
					<Header />
					<Searchbar />
				</Fragment>
			</Provider>
		)
	}
}

ReactDOM.render(<App />, document.getElementById('app'));