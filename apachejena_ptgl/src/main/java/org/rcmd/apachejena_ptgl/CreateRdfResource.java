

package org.rcmd.apachejena_ptgl;


/**
 * 
 * This roughly follows the Apache Jena RDF API tutorial, see https://jena.apache.org/tutorials/rdf_api.html
 */

 import org.apache.jena.rdf.model.Model;
 import org.apache.jena.rdf.model.ModelFactory;
 import org.apache.jena.rdf.model.Resource;
 import org.apache.jena.vocabulary.VCARD;

 public class CreateRdfResource {

    public static void createAuthor () {
        // some definitions
            final String personURI    = "http://somewhere/JohnSmith";
            final String fullName     = "John Smith";

            // create an empty Model
            Model model = ModelFactory.createDefaultModel();

            // create the resource
            Resource johnSmith = model.createResource(personURI);

            // add the property
            johnSmith.addProperty(VCARD.FN, fullName);
    }

 }

 