import React, { Component, Fragment } from 'react';

export default class Searchbar extends Component {
	render() {
		return (
			<Fragment>
				<div className="row">
				    <div className="col-8 offset-2" id="logo-container">
				        <span id="logo">SwapSpace</span>
				    </div>
				</div>
				<div className="row search-bar-row">
				    <div className="col-8 offset-2">
				        <div className="input-group mb-3">
				            <div className="input-group-prepend">
				                <button className="btn btn-outline-secondary dropdown-toggle" id="category-btn" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
				                    All
				                </button>
				                <div className="search-dropdown dropdown-menu">
				                    <a className="dropdown-item" href="#">
				                        <i className="fas fa-check"></i>
				                        All Departments
				                    </a>
				                    
				                </div>
				            </div>
				            <input type="hidden" name="search_param" value="all" id="search_param"/>
				            <input type="text" style={{height: 42+'px'}} className="form-control" name="x" placeholder="Search by keywords..."/>
				            <span className="input-group-btn">
				                <button className="btn btn-default" id="search-btn" type="button">
				                    <i className="fas fa-search"></i>
				                </button>
				            </span>
				        </div>
				    </div>
				</div>
				<hr id="header-hr" />
			</Fragment>
		);
	}
}
