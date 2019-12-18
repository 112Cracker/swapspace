import React, { Component } from "react";
import { connect } from "react-redux";

import PropTypes from "prop-types";
import { getCategory } from "../../actions/category";

export class Category extends Component {
	static propTypes = {
		category: PropTypes.array.isRequired
	}
	render() {
		return (

			);
	}
}

const mapStateToProps = state => ({
	category: state.category.category
});




export default connect(mapStateToProps, { getCategory })(Category);